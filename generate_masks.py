import cv2
import numpy as np
import os
from ultralytics import YOLO
MODEL_PATH = "/home/aagrimrautela/runs/segment/train4/weights/best.pt"
model = YOLO(MODEL_PATH)
PROMPT_MAP = {
    "segment taping area": 0,
    "segment joint/tape": 0,
    "segment drywall seam": 0,
    "segment crack": 1,
    "segment wall crack": 1
}
def create_rubric_mask(image_path, text_prompt, output_filename):
    class_id = PROMPT_MAP.get(text_prompt.lower())
    if class_id is None:
        print(f"Unknown prompt: '{text_prompt}'")
        return
    results = model(image_path, verbose=False)
    result = results[0]
    h, w = result.orig_img.shape[:2]
    final_mask = np.zeros((h, w), dtype=np.uint8)

    # success?
    if result.masks is not None:
        for i, mask in enumerate(result.masks.data):
            pred_class = int(result.boxes.cls[i].item())
            
            if pred_class == class_id:
                mask_np = mask.cpu().numpy()
                resized_mask = cv2.resize(mask_np, (w, h), interpolation=cv2.INTER_NEAREST)
                final_mask[resized_mask > 0] = 255

    cv2.imwrite(output_filename, final_mask)
    print(f"saved: {output_filename}")
if __name__ == "__main__":
    os.makedirs("submission_masks", exist_ok=True)
    test_img_1 = "test1.jpg"
    create_rubric_mask(
        image_path=test_img_1, 
        text_prompt="segment crack", 
        output_filename="segment_crack.png"
    )
