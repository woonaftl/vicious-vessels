(define (script-fu-ftl-black-shade    img
                                      drawable
									  shadow-radius
									  shadow-color
									  shadow-opacity)
  (let* (
        (shadow-layer 0)
        (image-width (car (gimp-image-width img)))
        (image-height (car (gimp-image-height img)))
        )
	
   (set! shadow-layer (car (gimp-layer-new img
										image-width
										image-height
										1
										"black shade"
										shadow-opacity
										0)))
	(gimp-image-set-active-layer img drawable)
	(gimp-image-insert-layer img shadow-layer 0 -1)
	(gimp-context-set-background shadow-color)
	(gimp-drawable-fill shadow-layer FILL-BACKGROUND)
	(gimp-drawable-edit-fill shadow-layer FILL-TRANSPARENT)
	(gimp-selection-none img)
	(gimp-layer-set-lock-alpha shadow-layer FALSE)
	(script-fu-tile-blur RUN-NONINTERACTIVE
                         img
						 shadow-layer
						 shadow-radius
						 TRUE
						 TRUE
						 _"IIR")
  )
)

(script-fu-register
  "script-fu-ftl-black-shade"         ;func name
  "FTL Black Shade WIP"                   ;menu label
  "Creates black shade on borders"    ;description
  "Me"                                ;author
  "Copyright 2018, Me"                ;copyright notice
  "Nov. 2018"                         ;date created
  "RGBA-IMAGE"                        ;image type that the script works on
  SF-IMAGE "Input Image" 0
  SF-DRAWABLE "Input Drawable" 0
  SF-ADJUSTMENT _"Radius"    '(50 0 1024 1 10 0 1)
  SF-COLOR      _"Color"          '(0 0 0)
  SF-ADJUSTMENT _"Opacity"        '(50 0 100 1 10 0 0)
)

(script-fu-menu-register "script-fu-ftl-black-shade"
                         "<Image>/Filters/My Filters")