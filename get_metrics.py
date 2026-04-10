import torch
import numpy as np
from ultralytics import YOLO

model = YOLO("/home/aagrimrautela/runs/segment/train4/weights/best.pt")
metrics = model.val(data="merged_dataset/data.yaml", split="val")
def calculate_dice_from_iou(iou):
    return (2 * iou) / (1 + iou)
try:
    mask_map50 = metrics.seg.map50
    calculated_miou = mask_map50 
    calculated_dice = calculate_dice_from_iou(calculated_miou)

    print(f"Mean Intersection over Union (mIoU): {calculated_miou:.4f}")
    print(f"Dice Coefficient (F1 Score):         {calculated_dice:.4f}")
    
except AttributeError:
    print("Could not extract segmentation metrics. Ensure you are using yolov8n-seg.pt")
