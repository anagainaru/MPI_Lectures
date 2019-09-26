class Complex():
    def __init__(self, real=0, img=0):
        self.real = real
        self.img = img

    def copy(self, num):
        self.real = num.real
        self.img = num.img

    def __repr__(self):
        return "Complex(%4.1f %4.1f)" %(self.real, self.img)

    def __str__(self):
        return "(%4.1f %4.1f)" %(self.real, self.img)
