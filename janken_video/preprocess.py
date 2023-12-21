from PIL import Image
import torch
from transformers import SamModel, SamProcessor
import skimage
import numpy as np 
import os 


# device ressources
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#--- Segment ---------------------------------------------------------------------------------------

# SAM model to segment and get the hand , see notebook for reference
model_name = r"shifumi_models/sam_model/"
processor_name = r"shifumi_models/sam_processor/"
model = SamModel.from_pretrained(model_name).to(device)
processor = SamProcessor.from_pretrained(processor_name)

# prompts to improve segmentation
input_point = np.array([[75,200]]) # x, y 
input_label = np.array([1,1])
input_boxes = [[[12, 50, 150, 300]]]

def embed(processor, model, image:Image,device:str = "cpu"):
    """
    Get the image's embedding
    """
    inputs = processor(image, return_tensors="pt").to(device)
    image_embeddings = model.get_image_embeddings(inputs["pixel_values"])

    return image_embeddings

def segment(processor, model, image:Image, image_embeddings,input_boxes:list, input_point:list,device:str = "cpu"):

    # preprocess the image with boxes 
    inputs = processor(image,input_boxes=input_boxes,input_point=input_point, return_tensors="pt").to(device)

    # pop the pixel_values as they are not neded
    inputs.pop("pixel_values", None)
    inputs.update({"image_embeddings": image_embeddings})

    # predict
    with torch.no_grad():
        outputs = model(**inputs)

    # masks[0] are masks see below to get one mask as 2D array 
    masks = processor.image_processor.post_process_masks(outputs.pred_masks.cpu(), inputs["original_sizes"].cpu(), inputs["reshaped_input_sizes"].cpu())
    # confidence scores
    scores = outputs.iou_scores

    max_score = np.argmax(np.array(scores[0][0]),axis=0)

    return masks, scores, max_score

#---MASKING -----------------------------------------------------------------------------------------
def get_mask(masks,idx:int)-> tuple :
    """
    Return a tuple of torch.Tensor : 
    (height,width,1) & (height,width) 
    The first tensor has just unsqueezed one dim 
    """

    # squeeze the batch size
    masks_squeezed = masks[0].squeeze()

    # First mask, float():bool-> 1,0 
    binary_mask =masks_squeezed[idx].float()

    # Height and Weight
    h, w = binary_mask.shape[-2:]

    # Add a third dim 
    mask_image = binary_mask.reshape(h, w, 1)

    return mask_image, binary_mask


#---WRAP UP-----------------------------------------------------------------------------------

def preprocess_image(image:np.array)->np.array:
    """
    
    """

    # resize the image 
    image_resized = Image.fromarray(image).resize((200,300))


    # 60 sec approx to run this cell 
    # run this once for multiple predictions 
    image_embeddings = embed(processor,model,image_resized)

    # extract the masks given the prompt
    masks, scores,max_score = segment(processor,
                        model,
                        image_resized,
                        image_embeddings,
                        input_boxes = input_boxes,
                        input_point = input_point,
                        )
    
    # from the mask with best score apply it
    mask_image, binary_mask = get_mask(masks,max_score)
    # (h,w,) -> (h,w,3)
    preprocessed_image = skimage.color.gray2rgb(binary_mask)

    h, w, c = preprocessed_image.shape
    # model expect (batch_size,h,w,3) => unsqueeze 
    unsqueezed_img= preprocessed_image.reshape((1,h,w,c))

    return unsqueezed_img
