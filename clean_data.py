import os
import glob

deleted = 0
bbox_warning = False
for cache_file in glob.glob("merged_dataset/*/labels/*.cache"):
    os.remove(cache_file)

for split in ['train', 'valid', 'test']:
    lbl_dir = f"merged_dataset/{split}/labels"
    img_dir = f"merged_dataset/{split}/images"
    
    if not os.path.exists(lbl_dir): continue
    
    for lbl_file in os.listdir(lbl_dir):
        lbl_path = os.path.join(lbl_dir, lbl_file)
        with open(lbl_path, 'r') as f:
            content = f.read().strip()
        if not content:
            os.remove(lbl_path)
            base_name = lbl_file.rsplit('.', 1)[0]
            for ext in ['.jpg', '.png', '.jpeg', '.JPG']:
                img_path = os.path.join(img_dir, base_name + ext)
                if os.path.exists(img_path):
                    os.remove(img_path)
            deleted += 1
            continue
            
        parts = content.split('\n')[0].split()
        if len(parts) == 5:
            bbox_warning = True

if bbox_warning:
    print("\n found bb, check dataset")
else:
    print("\n we cool")
