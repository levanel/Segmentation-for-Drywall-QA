import os
import shutil

CRACK_DIR = "crack_dataset"
JOINT_DIR = "joint_dataset"
OUT_DIR = "merged_dataset"

splits = ['train', 'valid', 'test']

for split in splits:
    os.makedirs(f"{OUT_DIR}/{split}/images", exist_ok=True)
    os.makedirs(f"{OUT_DIR}/{split}/labels", exist_ok=True)

def process_dataset(source_dir, split, target_class_id, prefix):
    img_dir = f"{source_dir}/{split}/images"
    lbl_dir = f"{source_dir}/{split}/labels"
    
    if not os.path.exists(img_dir): return

    for filename in os.listdir(img_dir):
        new_base = f"{prefix}_{filename}"
        img_src = os.path.join(img_dir, filename)
        img_dst = os.path.join(f"{OUT_DIR}/{split}/images", new_base)
        shutil.copy(img_src, img_dst)

        lbl_name = filename.rsplit('.', 1)[0] + ".txt"
        lbl_src = os.path.join(lbl_dir, lbl_name)
        lbl_dst = os.path.join(f"{OUT_DIR}/{split}/labels", f"{prefix}_{lbl_name}")

        if os.path.exists(lbl_src):
            with open(lbl_src, 'r') as f_in, open(lbl_dst, 'w') as f_out:
                for line in f_in:
                    parts = line.strip().split()
                    if len(parts) > 0:
                        parts[0] = str(target_class_id)
                        f_out.write(" ".join(parts) + "\n")

print("merging the datasets...")
for split in splits:
    print(f"processing {split}...")
    process_dataset(JOINT_DIR, split, target_class_id=0, prefix="jnt")
    
    process_dataset(CRACK_DIR, split, target_class_id=1, prefix="crk")
