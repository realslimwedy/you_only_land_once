import math
import numpy as np
import cv2 as cv
from scipy.spatial import distance
from scipy.ndimage.filters import gaussian_filter
from labels import datasetLabels, risk_table

class LzFinder:
    def __init__(self, dataset):
        self.dataset=dataset
        try:
            self.labels = datasetLabels[dataset]
        except:
            raise KeyError("Unsupported dataset name. Check your spelling.")

    def get_ranked_lz(
            self, obstacles, img, segImg, height=None, r_landing=120, stride=75, id=None, use_seg=True
    ):  # r_landing to be measured in pixels by testing
        # TODO: use height of drone to tune size of possible landing zones

        lzs = self._get_landing_zones_proposals(obstacles, stride, r_landing, img, id)
        risk_map = self._get_risk_map(segImg)
        lzs_ranked = self._rank_lzs(lzs, risk_map,obstacles)
        return lzs_ranked, risk_map

    def _dist_to_obs(self, lz, obstacles, img):
        posLz = lz.get("position")
        norm_dists = []
        if not obstacles:
            return 0
        else:
            for ob in obstacles:
                dist = self.getDistance(img, (ob[0], ob[1]), posLz)
                norm_dists.append(1-dist)
            return np.mean(norm_dists)

    def _meets_min_safety_requirement(cls, zone_proposed, obstacles_list):
        """Checks if a proposed safety zone is breaking the min. safe distance of all the high-risk obstacles detected in an image

        Args:
            zone_proposed (tuple): coordinates of the proposed zone in the x,y,r_landing format
            obstacles_list (list of tuples): list of coordinates of the high-risk obstacles in the x,y,r_min_safe_dist format

        Returns:
            (bool): True if it meets safety req., False otherwise.
        """
        posLz = zone_proposed.get("position")
        radLz = zone_proposed.get("radius")
        for obstacle in obstacles_list:
            touch = cls.circles_intersect(
                posLz[0], obstacle[0], posLz[1], obstacle[1], radLz, obstacle[2]
            )
            if touch < 0:
                return False
        return True

    def _get_landing_zones_proposals(self, high_risk_obstacles, stride, r_landing, image, id): # unsure what id is for
        """Returns list of lzs proposal based that meet the min safe distance of all the high risk obstacles

        :param high_risk_obstacles: tuple in the following format (x,y,min_safe_dist)
        :type high_risk_obstacles: tuple
        :param stride: how much stride between the proposed regions.
        :type stride: int
        :param r_landing: min safe landing radius - size of lz in pixels
        :type r_landing: int
        :param image: image to find lzs on
        :type image: Mat
        :return: list of lzs in the lz format
        :rtype: lz
        """
        zones_proposed = []

        for y in range(r_landing, image.shape[0] - r_landing, stride):
            for x in range(r_landing, image.shape[1] - r_landing, stride):
                lzProposed = {
                    "confidence": math.nan,
                    "radius": r_landing,
                    "position": (x, y),
                    "id": id,
                }
                if not self._meets_min_safety_requirement(
                        lzProposed, high_risk_obstacles
                ):
                    lzProposed["confidence"] = 0 # NaN means safe, zero means unsafe
                zones_proposed.append(lzProposed)
        return zones_proposed


    def _get_risk_map_slow(self, seg_img, windowsize, gaussian_sigma=7):
        risk_r = int(seg_img.shape[0] / windowsize)
        risk_c = int(seg_img.shape[1] / windowsize)
        risk_array = np.zeros(shape=(risk_r, risk_c))
        for r in range(0, seg_img.shape[0] - windowsize, windowsize):
            for c in range(0, seg_img.shape[1] - windowsize, windowsize):
                window = seg_img[r: r + windowsize, c: c + windowsize]
                risk_array[int(r / windowsize)][int(c / windowsize)] = self._get_risk(
                    window
                )

        risk_array = gaussian_filter(risk_array, sigma=gaussian_sigma)
        risk_array = (risk_array / risk_array.max()) * 255
        risk_array = np.uint8(risk_array)
        img = cv.resize(
            risk_array,
            (seg_img.shape[1], seg_img.shape[0]),
            interpolation=cv.INTER_CUBIC,
        )
        return img

    def _get_risk(self, image_segment):
        """Obtain a risk factor based on the section of an image.

        Args:
            image_segment (Mat): section of an image to be assessed. The assessment is based on the risk level defined in the risk_table.

        Returns:
            float: risk level. The higher, the riskier it is to land.
        """
        num_pix = image_segment.shape[0] * image_segment.shape[1]
        risk_level = 0
        for label in self.labels:
            label_pix = np.count_nonzero(
                (image_segment == self.labels[label]).all(axis=2)
            )
            ratio_label = label_pix / num_pix
            risk_level += ratio_label * risk_table[label].value
        return risk_level


    def _get_risk_map(self, seg_img, gaussian_sigma=25):
        image = seg_img
        risk_array = image.astype("float32") # also needed for yolo seg?
        for label in self.labels:
            np.where(risk_array == self.labels[label], risk_table[label], risk_array)
        risk_array = gaussian_filter(risk_array, sigma=gaussian_sigma)
        risk_array = (risk_array / risk_array.max()) * 255
        risk_array = np.uint8(risk_array)
        return risk_array

    def _risk_map_eval_basic(self, img, areaLz):
        """Evaluate normalised risk in a lz

        :param img: risk map containing pixels between 0 (low risk) and 255 (high risk)
        :type img: Mat
        :param areaLz: area of proposed lz
        :type areaLz: float
        :return: normalised risk [0.0, 1.0]
        :rtype: float
        """
        maxRisk = areaLz * 255
        totalRisk = np.sum(img)
        return 1 - (totalRisk / maxRisk)

    def _rank_lzs(self, lzsProposals, riskMap, obstacles, weightDist=5, weightRisk=15, weightOb=5):
        for lz in lzsProposals:

            lzRad = lz.get("radius")
            lzPos = lz.get("position")
            mask = np.zeros_like(riskMap) #  this is a numpy array of zeros with the same shape as riskMap
            mask = cv.circle(mask, (lzPos[0], lzPos[1]), lzRad, (255, 255, 255), -1) # cirlce drawn on mask, green, filled
            areaLz = math.pi * lzRad * lzRad
            crop = cv.bitwise_and(riskMap, mask) # returns crop

            riskFactor, distanceFactor, obFactor = 0, 0, 0
            if weightRisk != 0:
                riskFactor = self._risk_map_eval_basic(crop, areaLz)
            if weightDist != 0:
                distanceFactor = self.getDistanceCenter(riskMap, (lzPos[0], lzPos[1]))
            if weightOb != 0:
                obFactor = self._dist_to_obs(lz, obstacles, riskMap)

            if math.isnan(lz["confidence"]):
                # Calculate the confidence value and set it in the lz dictionary
                total_weight = weightRisk + weightDist + weightOb
                lz["confidence"] = abs(
                    (weightRisk * riskFactor + weightDist * distanceFactor + weightOb * obFactor) / total_weight)

            '''if lz["confidence"] is math.nan:
                lz["confidence"] = abs((
                                           weightRisk * riskFactor + weightDist * distanceFactor + weightOb * obFactor
                                   ) / (weightRisk + weightDist + weightOb))
                xxx = 0'''

        lzsSorted = sorted(lzsProposals, key=lambda k: k["confidence"])
        return lzsSorted

    def getDistanceCenter(self, img, pt):
        """Finds Normalised Distance between a given point and center of a frame

        :param img: image where the point resides
        :type img: Mat
        :param pt: coordinates of point in the form (x,y)
        :type pt: tuple
        :return: distance
        :rtype: float
        """
        dim = img.shape
        furthestDistance = math.hypot(dim[0] / 2, dim[1] / 2)
        dist = distance.euclidean(pt, [dim[0] / 2, dim[1] / 2])
        return 1 - abs(dist / furthestDistance)

    def getDistance(self, img, pt1, pt2):
        """Finds Normalised Distance between a two points

        :param img: image where the point resides
        :type img: Mat
        :param pt: coordinates of point in the form (x,y)
        :type pt: tuple
        :return: distance
        :rtype: float
        """
        dim = img.shape
        furthestDistance = math.hypot(dim[0], dim[1])
        dist = distance.euclidean(pt1, pt2)
        return 1 - abs(dist / furthestDistance) # 1 minus because we want to maximise the distance???

    @classmethod
    def draw_lzs_obs(cls, list_lzs, list_obs, img, thickness=3):
        """Adds annotation on image and landing zone proposals for visualisation

        :param list_lzs: list of lzs int the lz data struct
        :type list_lzs: list
        :param list_obs: list of obstacles in the obstacle format (x,y,min_safe_dist)
        :type list_obs: list
        :param img: image to add annotation on
        :type img: Mat
        :param thickness: thickness of circles, defaults to 3
        :type thickness: int, optional
        :return: image with added annotations
        :rtype: Mat
        """
        for obstacle in list_obs:
            cv.circle(
                img,
                (obstacle[0], obstacle[1]),
                obstacle[2],
                (0, 0, 255),
                thickness=thickness,
            )
        for lz in list_lzs:
            posLz = lz.get("position")
            radLz = lz.get("radius")
            cv.circle(
                img, (posLz[0], posLz[1]), radLz, (0, 255, 0), thickness=thickness
            )
        return img

    @classmethod
    def circles_intersect(cls, x1, x2, y1, y2, r1, r2):
        """Checks if two circle intersect

        :param x1: x-coordinate of first circle center
        :type x1: int
        :param x2: x-coordinate of second circle center
        :type x2: int
        :param y1: y-coordinate of first circle center
        :type y1: int
        :param y2: y-coordinate of second circle center
        :type y2: int
        :param r1: radius of first circle
        :type r1: int
        :param r2: radius of second circle
        :type r2: int
        :return: -3 (C2 is in C1), -2 (C1 is in C2), -1 (circles intersect), 0 (circles don't intersect)
        :rtype: int
        """

        d = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        if d < r1 - r2:
            # 'print("C2  is in C1")
            return -3
        elif d < r2 - r1:
            return -2
            # print("C1  is in C2")
        elif d > r1 + r2:
            return 0
            # print("Circumference of C1  and C2  intersect")
        else:
            return -1
            # print("C1 and C2  do not overlap")

if __name__="main":
    objectDetector = ObjectDetector(PATH_TO_MODEL)
    segEngine = SegmentationEngine(PATH_TO_MODEL)

    #start webcam
    cap = cv.VideoCapture(0)
    posOb= [0, 0, 0, 0]

    while True:
        ret, img = cap.read()
        height, width, _ = img.shape
        if not ret:
            break
        segImg= segEngine.segment(img)
        segImg=np.array(segImg)
        _, objs = objectDetector.infer_image(height, width, img)
        obstacles = []
        for obstacle in objs:
            print(obstacle)
            pos0b = obstacle.get("box")
            minDist = 100
            w, h = posOb[2], posOb[3]
            obstacles.append(
                [int(posOb[0] + w / 2), int(posOb[1] + h / 2), minDist]
            )

        lzFinder= LzFinder("aeroscapes")
        lzs_ranked, risk_map = lzFinder.get_ranked_lz(obstacles, img, segImg)
        img = lzFinder.draw_lzs_obs(lzs_ranked[-5:], obstacles, img)

        cv.imshow("best landing zones", cv.applyColorMap(risk_map, cv.COLORMAP_JET))
        cv.waitKey(0)
        cv.imshow("best landing zones", img)
        cv.waitKey(0)
        cv.destroyAllWindows()