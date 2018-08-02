from PIL import Image
import os
import glob

def crop(infile,height,width):
    im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(imgheight//height):
        for j in range(imgwidth//width):
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)

def save_cropped_images(infile, outfolder, height, width, start_num):
    for k, piece in enumerate(crop(infile, height, width), start_num):
        img = Image.new('RGB', (height, width), 255)
        img.paste(piece)
        path = os.path.join(outfolder, "%02d.png" % k)
        print(path+' from '+infile)
        img.save(path)

def crop_all_images(all_images, outfolder, height, width, start_num, number_of_pieces):
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)

    list_images = sorted(glob.glob(all_images))
    for image in list_images:
        save_cropped_images(image, outfolder, height, width, start_num)
        start_num = start_num + number_of_pieces

def main():
    height = 512
    width = 512
    start_num = 0
    number_of_pieces = 4

    os.chdir('datasets')

    infolder = 'vnc/stack1/raw/*.png'
    outfolder = 'cropped_vnc/stack1/raw'
    crop_all_images(infolder, outfolder, height, width, start_num, number_of_pieces)

    infolder = 'vnc/stack1/labels/*.png'
    outfolder = 'cropped_vnc/stack1/labels'
    crop_all_images(infolder, outfolder, height, width, start_num, number_of_pieces)

    infile = 'cortex/stack1/raw/49.png'
    outfolder = 'cropped_cortex/stack1/raw'
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    save_cropped_images(infile, outfolder, height, width, start_num)

    infile = 'cortex/stack1/labels/49.png'
    outfolder = 'cropped_cortex/stack1/labels'
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    save_cropped_images(infile, outfolder, height, width, start_num)






main()