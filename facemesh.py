import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
mp_drawing = mp.solutions.drawing_utils

MOUTH_LEFT = 61
MOUTH_RIGHT = 291
MOUTH_TOP = 0
MOUTH_BOTTOM = 17


def detectar_emocion(landmarks, width, height):
    mouth_left = (int(landmarks[MOUTH_LEFT].x * width), int(landmarks[MOUTH_LEFT].y * height))
    mouth_right = (int(landmarks[MOUTH_RIGHT].x * width), int(landmarks[MOUTH_RIGHT].y * height))
    mouth_top = (int(landmarks[MOUTH_TOP].x * width), int(landmarks[MOUTH_TOP].y * height))
    mouth_bottom = (int(landmarks[MOUTH_BOTTOM].x * width), int(landmarks[MOUTH_BOTTOM].y * height))
    
    mouth_width = mouth_right[0] - mouth_left[0]
    mouth_height = mouth_bottom[1] - mouth_top[1]
    mouth_ratio = mouth_height / mouth_width  
    print(mouth_width, mouth_height, mouth_ratio)
    
    if mouth_ratio < 0.27: # umbral ajustablre
        return "Feliz"
    else:
        return "Triste"


cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                frame, 
                face_landmarks, 
                mp_face_mesh.FACEMESH_TESSELATION,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1),
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1)
            )
            
            height, width, _ = frame.shape
            emocion = detectar_emocion(face_landmarks.landmark, width, height)
        
            text = f"Emocion: {emocion}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            thickness = 2
            text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
            text_w, text_h = text_size
            x, y = 200, 50

            cv2.rectangle(frame, (x, y - text_h - 10), (x + text_w, y + 10), (0, 0, 0), cv2.FILLED)
            cv2.putText(frame, text, (x, y), font, font_scale, (0, 0, 255), thickness)

    cv2.imshow("Deteccion de emociones", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
