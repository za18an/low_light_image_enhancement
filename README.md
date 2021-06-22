# Low Light Image Enhancement
This python script is based on the implementation concenpt of haze removal from Zhiming Tan Et al. [Research Paper](https://pdfs.semanticscholar.org/64ca/a24f2cb3fff6d8eb966f90078f0d0b8a7db0.pdf)

## Image Enhancement Technique
The whole technique is based on three steps,
1.  Inverting the low light image
2.  Applying the Haze Removal technique on the inverted image
3.  Invert the enhanced image

## Haze Removal
The removal part comprises of three steps,
1.  Determine the intensity of atmospheric light. *
2.  Estimate transmission map.
3.  Clarify image.

* This in our case is constant which is 255, obtain from experimenting on multiple images. This will be updated so that it is calculated through a function. Si
nce it was taking too long to compute this value it is better to find the average value of a batch.

Intensity of atmospheric light `A` is estimated form hazed image `I(x)`
Transmission map `t(x)` is estimated using `A` and `I(x)`
Image is clarified with the image defogging model

#### Estimate intensity of atmospheric light:
Finding the top 0.1% brightest pixels in the dark channel then choose one with highest intensity as the representing of atmospheric light. `This part is not needed in our case and thus ignored`

#### Estimate transmission map:
Find a dark channel based on a local area(coarsemap)
Then, the transmission map `t(x)` is thereby obtained:

```t(x) = 1 – defoggingParam * darkPixelFromCoarseMap / AtmosphericLightIntensity```

The ```defoggingParam``` is a value between 0 to 1. The higher value the lesser amount of fog would be kept for the distant objects.

#### Clarify image:
The image is clarified by: ```J(x)=(I(x)- A)/max(t(x), t0)+A```

Where `J(x)` is output, `I(x)` is input, `t(x)` is transmission map, `A` is atmospheric light and `t0` is set to a constant value to avoid dividing by zero.

#### Usage:
Currently, the user has to specify the input image and output image path in a main() function. Next update will use console arguments to specify the image path. Feel free to add new things to the code and pull a merge request.

#### Dependencies
cv2
numpy
