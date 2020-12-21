
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

from PySide2 import QtMultimedia
from PySide2 import QtMultimediaWidgets


class DDSVideoSurface(QtMultimedia.QAbstractVideoSurface):
    '''
    '''
    def __init__(self, view, scene):
        super().__init__()
        
        self.view = view
        self.scene = scene
        self.imageFormat = QtGui.QImage.Format_Invalid
        
        #self.pixmapItem = QtWidgets.QGraphicsPixmapItem()
        #self.scene.addItem(self.pixmapItem)

    def present(self, frame):
        '''
        frame: 
            QVideoFrame object
        '''
        print("present frame...")
        
        img = self.videoframe_to_image(frame)
        self.displayframe(img)
        
        return True

    def supportedPixelFormats(self, handle_type):
        '''
        handle_type:
            QAbstractVideoBuffer.HandleType object
        '''
        result = []
        
        if handle_type == QtMultimedia.QAbstractVideoBuffer.NoHandle:
            result [
                QtMultimedia.QVideoFrame.Format_ARGB32,
                QtMultimedia.QVideoFrame.Format_ARGB32_Premultiplied,
                QtMultimedia.QVideoFrame.Format_RGB32,
                QtMultimedia.QVideoFrame.Format_RGB24,
                QtMultimedia.QVideoFrame.Format_RGB565,
                QtMultimedia.QVideoFrame.Format_RGB555,
                QtMultimedia.QVideoFrame.Format_ARGB8565_Premultiplied,
                QtMultimedia.QVideoFrame.Format_BGRA32,
                QtMultimedia.QVideoFrame.Format_BGRA32_Premultiplied,
                QtMultimedia.QVideoFrame.Format_BGR32,
                QtMultimedia.QVideoFrame.Format_BGR24,
                QtMultimedia.QVideoFrame.Format_BGR565,
                QtMultimedia.QVideoFrame.Format_BGR555,
                QtMultimedia.QVideoFrame.Format_BGRA5658_Premultiplied,
                QtMultimedia.QVideoFrame.Format_AYUV444,
                QtMultimedia.QVideoFrame.Format_AYUV444_Premultiplied,
                QtMultimedia.QVideoFrame.Format_YUV444,
                QtMultimedia.QVideoFrame.Format_YUV420P,
                QtMultimedia.QVideoFrame.Format_YV12,
                QtMultimedia.QVideoFrame.Format_UYVY,
                QtMultimedia.QVideoFrame.Format_YUYV,
                QtMultimedia.QVideoFrame.Format_NV12,
                QtMultimedia.QVideoFrame.Format_NV21,
                QtMultimedia.QVideoFrame.Format_IMC1,
                QtMultimedia.QVideoFrame.Format_IMC2,
                QtMultimedia.QVideoFrame.Format_IMC3,
                QtMultimedia.QVideoFrame.Format_IMC4,
                QtMultimedia.QVideoFrame.Format_Y8,
                QtMultimedia.QVideoFrame.Format_Y16,
                QtMultimedia.QVideoFrame.Format_Jpeg,
                QtMultimedia.QVideoFrame.Format_CameraRaw,
                QtMultimedia.QVideoFrame.Format_AdobeDng
            ]
            
        return result
    
    def isFormatSupported(self, xformat):
        '''
        format: 
            QVideoSurfaceFormat object
        '''
        print("isFormatSupported...")
        imageFormat = QtMultimedia.QVideoFrame.imageFormatFromPixelFormat(xformat.pixelFormat())
        size = xformat.frameSize()

        return imageFormat != QtGui.QImage.Format_Invalid \
            and not size.isEmpty() \
            and xformat.handleType() == QtMultimedia.QAbstractVideoBuffer.NoHandle
            
        #return True
    
    def displayframe(self, img):
        '''
        img:
            QImage object
        '''
        self.pixmap.setPixmap(QtGui.QPixmap.fromImage(img))
        self.view.fitInView(QtCore.QRectF(0,0,img.width(), img.height()), 
                            QtCore.Qt.KeepAspectRatio)
        
        self.view.update()
    
    def videoframe_to_image(self, frame):
        '''
        frame:
            QVideoFrame object
        
        return QImage object
        '''
        if frame.map(QtMultimedia.QAbstractVideoBuffer.ReadOnly):
            return QtGui.QImage(frame.bits(), frame.width(), frame.height(), frame.bytesPerLine(), self.imageFormat)
    
        return QtGui.QImage()
    
    def start(self, xformat):
        '''
        format:
            QVideoSurfaceFormat object
            
        return 
            bool
        '''
        imageFormat = QtMultimedia.QVideoFrame.imageFormatFromPixelFormat(xformat.pixelFormat())
        size = xformat.frameSize()

        if imageFormat != QtGui.QImage.Format_Invalid and not size.isEmpty() :
            self.imageFormat = imageFormat
            super().start(xformat)
            return True
        else:
            return False
    
    def stop(self):
        '''
        '''
        super().stop()
        self.view.update()


class DDSVideoScene(QtWidgets.QGraphicsScene):
    '''
    '''
    def __init__(self, view):
        '''
        '''
        QtWidgets.QGraphicsScene.__init__(self)
        
        self.view = view
        
        self.view.setScene(self)
        
        #self.videoItem = QtMultimediaWidgets.QGraphicsVideoItem()
        #self.addItem(self.videoItem)
    
        
