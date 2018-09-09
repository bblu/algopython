# -*- coding: utf-8 -*-

#import convexHull as Convex
import json
from pg import DB
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull as Convex


pgcnn=DB(dbname='fzgis',host='localhost',port=5432,user='postgres',passwd='123456')

def drawHull(pts,idxs):
    x=[]
    y=[]
    for i in idxs:
        x.append(pts[i][0])
        y.append(pts[i][1])
    x.append(x[0])
    y.append(y[0])
    plt.plot(x,y,color='red')
    plt.show()

fo = open("test.txt", "w")
def wo(item_id,pts,idx):
    global fo
    coord = []
    for i in idx:
        coord.append(pts[i])
    coord.append(coord[0])
    print item_id,len(coord),coord
    fo.write('%s@%s\n'%(item_id,coord))

def wb(item_id,pts):
    global fo
    x0 = min(pts[0][0], pts[1][0])
    y0 = min(pts[0][1], pts[1][1])
    x1 = max(pts[0][0], pts[1][0])
    y1 = max(pts[0][1], pts[1][1])
    pts=[]
    pts.append([x0, y0])
    pts.append([x1, y0])
    pts.append([x1, y1])
    pts.append([x0, y1])
    pts.append([x0, y0])
    print item_id, '-2-', pts
    fo.write('%s@%s\n' % (item_id, pts))

def genSql(item_id):
    global pgcnn
    sql = "select geom from equ_xl_dev where item_id = '%s'" % item_id
    columns = pgcnn.query(sql).namedresult()
    pts=[]
    for tup in columns:
        #print tup.geom
        geo = json.loads(tup.geom)
        typ = geo['type']
        #print typ
        cds = geo['coordinates']
        if typ == 'LineString':
            pts += cds
        else:
            for sub in cds:
                pts += sub
    print item_id,len(pts),
    if len(pts)>2:
        hull = Convex(pts)
        idxs = hull.vertices
        #idxs.append(idxs[0])
        print len(hull.vertices),hull.vertices
        #drawHull(pts,idxs)
        wo(item_id,pts,idxs)
    elif len(pts)==2:
        print '*****************************'
        wb(item_id,pts)

pgtbs=pgcnn.query('select distinct item_id from equ_xl_dev order by item_id;')

for row in pgtbs.namedresult():
    genSql(row.item_id)
    #genSql("0016001200c5")
    #break

#测试
if __name__ == '__main__':
    ps = [[2, 2],[1, 1],[2, 1],[1.5, 1.5],[1, 2],[3, 1.5],[1.5, 1.2],[0.5, 2],[1.5, 0.5]]

    #[{'y': 0.5, 'x': 1.5}, {'y': 1.5, 'x': 3}, {'y': 2, 'x': 2}, {'y': 2, 'x': 1}, {'y': 2, 'x': 0.5}, {'y': 1, 'x': 1}]
    #print Convex.graham_scan(ps)

