(define (script-fu-ftl-white-crop    img
                               drawable)
  (let* (
        (current-layer 0)
		(current-selection 0)
		(pink '(255 170 186))
        )
    
	(gimp-image-select-color img 2 drawable '(255 255 255))
    (gimp-edit-clear drawable)
    (gimp-selection-invert img)
    (plug-in-autocrop RUN-NONINTERACTIVE img drawable)
    (script-fu-ftl-shadow img drawable 0 0 25 pink 25 TRUE)
  )
)

(script-fu-register
  "script-fu-ftl-white-crop"                ;func name
  "FTL White Crop"                          ;menu label
  "Crops white bg and adds glow"    ;description
  "Me"                                ;author
  "Copyright 2018, Me"                ;copyright notice
  "Nov. 2018"                         ;date created
  ""                                  ;image type that the script works on
  SF-IMAGE "Input Image" 0
  SF-DRAWABLE "Input Drawable" 0
)

(script-fu-menu-register "script-fu-ftl-white-crop"
                         "<Image>/Filters/My Filters")