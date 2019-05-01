; TO USE
; run terminal from folder which contains gib png images with white borders and nothing else
; gimp -i -b '(batch-ftl-white-crop "*.png")' -b '(gimp-quit 0)'


(define (batch-ftl-white-crop pattern)
(let* ((filelist (cadr (file-glob pattern 1))))
(while (not (null? filelist))
(let* ((filename (car filelist))
(image (car (gimp-file-load RUN-NONINTERACTIVE filename filename)))
(drawable (car (gimp-image-get-active-layer image))))
; Modify the stuff below, add/remove filters
(script-fu-ftl-white-crop image drawable)
; Modify above
(set! drawable (car (gimp-image-merge-visible-layers image TRUE)))
(gimp-file-save RUN-NONINTERACTIVE image drawable filename filename)
(gimp-image-delete image)
)
(set! filelist (cdr filelist))
)
)
)