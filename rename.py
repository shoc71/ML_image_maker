from PIL import Image
import os

def imageRewrite(filepath, input_name): 
    files = os.listdir(filepath)

    names_list = [filepath + file for file in files]

    for name in names_list:
        if "test" in name:
            print("Test found. Image skipped.")
            continue
        else:
            img = Image.open(name)
            name = name.replace(filepath, '')
            print(name)
            new_name = filepath + input_name + name
            img.save(new_name)
            print(f"Image {new_name} Renamed Successfully!")
            
    img.close()

if __name__ == "__main__":
    # main()
    pass