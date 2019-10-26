import sys
import skimage as ski
import matplotlib.pyplot as plt

from skimage import io, color, data


def show_img_and_mask(img, mask):

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10,10))
    
    ax1.imshow(img)
    ax1.set_axis_off()
    ax2.imshow(mask, cmap=plt.cm.gray)
    ax2.set_axis_off()
    
    plt.show()


def chroma_key_mask( img, x, y , th, ts, tv ):

    img_hsv = color.rgb2hsv(img)

    h,s,v = img_hsv[x,y,:]
    maskh = (img_hsv[:,:,0] <= h+th).__and__(img_hsv[:,:,0] >= h-th)
    masks = (img_hsv[:,:,1] <= s+ts).__and__(img_hsv[:,:,1] >= s-ts)
    maskv = (img_hsv[:,:,2] <= v+tv).__and__(img_hsv[:,:,2] >= v-tv)
    
    maskbackh = (img_hsv[:,:,0] >= 0).__and__(img_hsv[:,:,0] <=0.01)
    maskbacks = (img_hsv[:,:,1] >= 0).__and__(img_hsv[:,:,1] <=0.01)
    maskbackv = (img_hsv[:,:,2] >= 0).__and__(img_hsv[:,:,2] <=0.01)
    
    maskback = maskbackh.__and__(maskbacks).__and__(maskbackv)
    mask = maskh.__and__(masks).__and__(maskv)
    mask = mask.__or__(maskback)
    
    return mask.astype(int)


if __name__ == "__main__":
    
    img = ski.img_as_float(color.gray2rgb(data.camera()))
    mask = chroma_key_mask(img, 60, 60, .2, .2, .2)

    show_img_and_mask(img, mask)
