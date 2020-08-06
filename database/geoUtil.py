# geoUtil.py by bblu @ 2018-03-26
import math


class geoUtil:
    # deal with geoJson object,substract and to svg
    __slots__ = ['buff', 'svg_circle', 'svg_text']

    def __init__(self):
        self.buff = ''
        self.svg_circle = '<circle x="%s" y="%s" r="%s" fill="red" stroke="red" stroke-width="3" fill-opacity="0.5"/>\n'
        self.svg_text = '<text x=%s y=%s font-size="%s" >%s</text>\n'

    #pa such as geo['coordinates'][i-1:i+2]
    def angle(pa):
        vx = pa[0][0] - pa[1][0]
        vy = pa[0][1] - pa[1][1]
        px = pa[1][0] - pa[2][0]
        py = pa[1][1] - pa[2][1]
        a1 = math.atan2(vy, vx)
        a2 = math.atan2(py, px)
        return a2 - a1

    def degrees(self, pa):
        return (self.getAngle(pa) * 180)/math.pi

    def distance2(pa):
        return (pa[1][0]-pa[0][0])**2 + (pa[1][0]-pa[0][0])**2

    def distance2xe5(pa):
        return ((pa[1][0] - pa[0][0]) ** 2 + (pa[1][0] - pa[0][0]) ** 2) * 1e5

    def substractlinestring(self, coord, opt):
        maxA = opt.maxAngle
        max2A = maxA * 2
        maxD = opt.maxDista
        keepA = 0
        keepD = 0
        pl = len(coord)
        lastA = range(1, pl)
        dis2A = range(1, pl)
        delpt = []
        for i in range(1, pl-1):
            lastA[i] = self.degrees(coord[i-1:i+2])
            dis2A[i] = self.distance2xe5(coord[i-1:i+1])
            if lastA[i] < maxA:
                if i > 4:
                    accA = lastA[i-4] + lastA[i-3] + lastA[i-2] + lastA[i-1]
                    if accA > max2A:
                        keepA += 1
                        lastA[i] = 0
                        continue
                    accD = dis2A[i-4] + dis2A[i-3] + dis2A[i-2] + dis2A[i-1]
                    if accD > maxD:
                        keepD += 1
                        dis2A[i] = 0
                        continue
                delpt.append(i)
            else:
                lastA[i] = 0
                dis2A[i] = 0
        sl = len(delpt)
        if sl < 1:
            return 0
        delpt = delpt[::-1]
        for i in delpt:
            del coord[i]
        print '|-maxA=%s [Ka=%s, Kd=%s] ptNum = %s - %s = %s [%.2f%%]'%(maxA,
                                    keepA, keepD, pl, sl, pl-sl, (sl*100.0)/pl)

    def substractlinereverse(self, coord, opt):
        maxa = opt.maxAngle
        max2a = maxa * 2
        maxd = opt.maxDista
        keepbyang = 0
        keepbydis = 0
        deletenum = 0
        pl = len(coord)
        lasta = range(1, pl)
        dis2a = range(1, pl)
        for i in range(pl-2, 0, -1):
            lasta[i] = self.degrees(coord[i-1:i+2])
            dis2a[i] = self.distance2xe5(coord[i:i+2])
            if lasta[i] < maxa:
                if pl - i > 4:
                    acca = lasta[i+1] + lasta[i+2] + lasta[i+3] + lasta[i+4]
                    if acca > max2a:
                        keepbyang += 1
                        lasta[i] = 0
                        continue
                    accd = dis2a[i+1] + dis2a[i+2] + dis2a[i+3] + dis2a[i+4]
                    if accd > maxd:
                        keepbydis += 1
                        dis2a[i] = 0
                        continue
                deletenum += 1
                del coord[i]
            else:
                lasta[i] = 0
                dis2a[i] = 0
        leftnum = len(coord)

        print '|-maxA=%s [Ka=%s, Kd=%s] ptNum=%s - %s = %s [%.2f%%]'%(maxa,
                        keepbyang, keepbydis, pl, sl, leftnum,(leftnum*100.0)/pl)

    def substractmultiline(self, coord, opt):
        pass

    def substract(self, geo, opt):
        if geo['type']=='LineString':
            self.substractlinestring(geo['coordinates'],opt)
        elif geo['type']=='MultiLineString':
            # todo: change multilinestring with one segment to Linestring
            for line in geo['coordinates']:
                self.substractlinestring(line,opt)

    def linestring2svg(self,coord,opt):
        pl = len(coord)
        i = 0
        r = 3
        pt = coord[i]
        self.buff += self.svg_circle % (pt[0],pt[1],5)

        for i in range(1,pl-1):
            pt = coord[i]
            self.buff += self.svg_circle % (pt[0], pt[1], 3)
            txt = i
            if opt.showAngle:
                txt = '%s:%s'%(i,self.angle(coord[i-1:i+1]))
            elif opt.showDegree:
                txt = '%s:%s' % (i, self.degrees(coord[i - 1:i + 1]))
            self.buff += self.svg_text %(pt[0], pt[1],txt)

        pt = coord[i+1]
        self.buff += self.svg_circle % (pt[0], pt[1])

    def multiline2svg(self,coord,opt):
        pass
    '''
    opt.W, opt.H
    opt.ptSize = 3,5,...
    opt.showAngle, opt.showDegree
    '''
    def svgstring(self, geo, opt):
        w = 1024
        h = 768
        if opt.W :
            w, h = opt.w, opt.h
        self.buff = '<svg width="%s" height="%s" version="1.1">\n'%(w,h)

        if geo['type']=='LineString':
            self.linestring2svg(geo['coordinates'], opt)
        elif geo['type']=='MultiLineString':
            self.multiline2svg(geo['coordinates'], opt)

