from model import config
import sys
import os
import torch
import cv2

# load our object detector, set it evaluation mode, and label
# encoder from disk
print("**** loading object detector...")
model = torch.load(config.LAST_MODEL_PATH).to(config.DEVICE)
model.eval()

data = []
for path in sys.argv[1:]:
    if path.endswith('.csv'):
        # loop over CSV file rows (filename, startX, startY, endX, endY, label)
        for row in open(path).read().strip().split("\n"):
            # TODO: read bounding box annotations
            filename, _, _, _, _, label = row.split(',')
            filename = os.path.join(config.IMAGES_PATH, label, filename)
            # TODO: add bounding box annotations here
            data.append((filename, None, None, None, None, label))
    else:
        data.append((path, None, None, None, None, None))

# loop over images to be tested with our model, with ground truth if available
# TODO: must read bounding box annotations once added
for filename, gt_start_x, gt_start_y, gt_end_x, gt_end_y, gt_label in data:
    # load the image, copy it, swap its colors channels, resize it, and
    # bring its channel dimension forward
    image = cv2.imread(filename)
    display = image.copy()
    h, w = display.shape[:2]

    # convert image to PyTorch tensor, normalize it, upload it to the
    # current device, and add a batch dimension
    image = config.TRANSFORMS(image).to(config.DEVICE)
    image = image.unsqueeze(0)

    # predict the bounding box of the object along with the class label
    # TODO: need to retrieve label AND bbox predictions once added in network
    label_predictions = model(image)

    # determine the class label with the largest predicted probability
    label_predictions = torch.nn.Softmax(dim=-1)(label_predictions)
    most_likely_label = label_predictions.argmax(dim=-1).cpu()
    label = config.LABELS[most_likely_label]

    # TODO:denormalize bounding box from (0,1)x(0,1) to (0,w)x(0,h)

    # draw the ground truth box and class label on the image, if any
    if gt_label is not None:
        cv2.putText(display, 'gt ' + gt_label, (0, h - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 0,  0), 2)
        # TODO: display ground truth bounding box in blue

    # draw the predicted bounding box and class label on the image
    cv2.putText(display, label, (0, 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
    # TODO: display predicted bounding box, don't forget tp denormalize it!

    # show the output image
    cv2.imshow("Output", display)

    # exit on escape key or window close 
    key = -1
    while key == -1:
        key = cv2.waitKey(100)
        closed = cv2.getWindowProperty('Output', cv2.WND_PROP_VISIBLE) < 1
        if key == 27 or closed:
           exit(0)
