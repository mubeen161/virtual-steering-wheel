import math
import keyinput
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
font = cv2.FONT_HERSHEY_SIMPLEX
# 0 For webcam input:
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5, 
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, video = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the video as not writeable to
    video.flags.writeable = False
    video = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
    results = hands.process(video)
    videoHeight, videoWidth, _ = video.shape

    # Draw the hand annotations on the video.
    video.flags.writeable = True
    video = cv2.cvtColor(video, cv2.COLOR_RGB2BGR)
    co=[]
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            video,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
        for point in mp_hands.HandLandmark:
           if str(point) == "HandLandmark.WRIST":
              normalizedLandmark = hand_landmarks.landmark[point]
              pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x,
                                                                                        normalizedLandmark.y,
                                                                                    videoWidth, videoHeight)

              try:
                co.append(list(pixelCoordinatesLandmark))
              except:
                  continue

    if len(co) == 2:
        xm, ym = (co[0][0] + co[1][0]) / 2, (co[0][1] + co[1][1]) / 2
        radius = 150
        try:
            m=(co[1][1]-co[0][1])/(co[1][0]-co[0][0])
        except:
            continue
        x1=co[0][0]
        y1=co[0][1]
        x2=co[1][0]
        y2=co[1][1]
        a = 1 + m ** 2
        b = -2 * xm - 2 * x1 * (m ** 2) + 2 * m * y1 - 2 * m * ym
        c = xm ** 2 + (m ** 2) * (x1 ** 2) + y1 ** 2 + ym ** 2 - 2 * y1 * ym - 2 * y1 * x1 * m + 2 * m * ym * x1 - 22500
        xa = (-b + (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
        xb = (-b - (b ** 2 - 4 * a * c) ** 0.5) / (2 * a)
        ya = m * (xa - x1) + y1
        yb = m * (xb - x1) + y1
        if m!=0:
          ap = 1 + ((-1/m) ** 2)
          bp = -2 * xm - 2 * xm * ((-1/m) ** 2) + 2 * (-1/m) * ym - 2 * (-1/m) * ym
          cp = xm ** 2 + ((-1/m) ** 2) * (xm ** 2) + ym ** 2 + ym ** 2 - 2 * ym * ym - 2 * ym * xm * (-1/m) + 2 * (-1/m) * ym * xm - 22500
          try:
           xap = (-bp + (bp ** 2 - 4 * ap * cp) ** 0.5) / (2 * ap)
           xbp = (-bp - (bp ** 2 - 4 * ap * cp) ** 0.5) / (2 * ap)
           yap = (-1 / m) * (xap - xm) + ym
           ybp = (-1 / m) * (xbp - xm) + ym

          except:
              continue

        cv2.circle(img=video, center=(int(xm), int(ym)), radius=radius, color=(195, 255, 62), thickness=15)

        l = (int(math.sqrt((x1 - x2) ** 2 * (y1 - y2) ** 2)) - 150) // 2
        cv2.line(video, (int(xa), int(ya)), (int(xb), int(yb)), (195, 255, 62), 20)
        if x1 > x2 and y1>y2 and y1 - y2 > 65:
            print("Turn left.")
            # keyinput.release_key('s')
            # keyinput.release_key('d')
            keyinput.press_key('a')
            cv2.putText(video, "Turn left", (50, 50), font, 0.8, (0, 255, 0), 2)
            cv2.line(video, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 20)


        elif x2 > x1 and y2> y1 and y2 - y1 > 65:
            print("Turn left.")
            # keyinput.release_key('s')
            # keyinput.release_key('d')
            keyinput.press_key('a')
            cv2.putText(video, "Turn left", (50, 50), font, 0.8, (0, 255, 0), 2)
            cv2.line(video, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 20)


        elif x1 > x2 and y2> y1 and y2 - y1 > 65:
            print("Turn right.")
            # keyinput.release_key('s')
            # keyinput.release_key('a')
            keyinput.press_key('d')
            cv2.putText(video, "Turn right", (50, 50), font, 0.8, (0, 255, 0), 2)
            cv2.line(video, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 20)

        elif x2 > x1 and y1> y2 and y1 - y2 > 65:
            print("Turn right.")
            # keyinput.release_key('s')
            # keyinput.release_key('a')
            keyinput.press_key('d')
            cv2.putText(video, "Turn right", (50, 50), font, 0.8, (0, 255, 0), 2)
            cv2.line(video, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 20)
        
        else:
            print("keeping straight")
            # keyinput.release_key('s')
            # keyinput.release_key('a')
            # keyinput.release_key('d')
            keyinput.press_key('w')
            cv2.putText(video, "keep straight", (50, 50), font, 0.8, (0, 255, 0), 2)
            if ybp>yap:
                cv2.line(video, (int(xbp), int(ybp)), (int(xm), int(ym)), (195, 255, 62), 20)
            else:
                cv2.line(video, (int(xap), int(yap)), (int(xm), int(ym)), (195, 255, 62), 20)

    if len(co)==1:
       print("keeping back")
    #    keyinput.release_key('a')
    #    keyinput.release_key('d')
    #    keyinput.release_key('w')
       keyinput.press_key('s')
       cv2.putText(video, "keeping back", (50, 50), font, 1.0, (0, 255, 0), 2)

    cv2.imshow('MediaPipe Hands', cv2.flip(video, 1))

# Flip the video horizontally for a selfie-view display.
    if cv2.waitKey(5) & 0xFF == ord('q'):
      break
cap.release()
