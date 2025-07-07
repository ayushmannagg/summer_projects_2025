import numpy as np
import cv2

black_screen = np.zeros((700,800))
cv2.line(black_screen, (100,100),(500,500), (255,25,255),3 )
cv2.rectangle(black_screen, (50,50), (500,500),(255,255,255), -1)

cv2.imshow("xyz", black_screen)

cv2.waitKey(0)

black_screen.release()
cv2.destroyAllWindows()