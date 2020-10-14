
from laspy.file import File
from pyproj import Transformer

def main():
    f = File("F:/data/112048g.las", mode='r')

    # 查看点云的点格式及字段名称
    print('\nPoint Of Data Format: ', f.header.data_format_id)
    print("\tExamining Point Format: ", end=" ")
    for spec in f.point_format:
        print(spec.name, end=", ")

    print('\noffset: ', f.header.offset)  # 偏移量
    print('scale: ', f.header.scale)  # 比例因子
    print('min: ', f.header.min)  # x、y、z 的最小值
    print('max: ', f.header.max)  # x、y、z 的最大值
    print('file_signature: ', f.header.file_signature)  # 文件标识
    print('Point Of Data Format: ', f.header.data_format_id)  # 点格式
    print('cell_Format_length: ', f.header.data_record_length)  # 点个数
    print('data_Records_count: ', f.header.records_count)
    print('FileCreateDay+Year: ', f.header.date)
    print()

    #print('f.x: ', f.x)
    #print('f.y: ', f.y)
    #print('f.z: ', f.z)
    r = 111201
    t = Transformer.from_crs(4326,2359)
    points=[]
    for i in range(0,10):
        i*=2000
        print(f.x[i],f.y[i],f.z[i])
        print((f.x[i]-f.header.min[0])*r,(f.y[i]-f.header.min[1])*r,f.z[i])
        points.append((f.y[i],f.x[i],f.z[i]))

    for pt in t.itransform(points):
        print('{:.3f} {:.3f}'.format(*pt))
    
    #print('f.intensity: ', f.intensity)
    #print('f.gps_time: ', f.gps_time)
    #print('f.raw_classification: ', f.raw_classification)
    print()
    # print('f.user_data: ', f.user_data)
    # print('f.flag_byte: ', f.flag_byte)
    # print('f.Color: ', f.red, f.green, f.blue)

    # print('file_source_id: ', f.header.file_source_id)
    # print('Major_Minor version: ', f.header.version, str(f.header.version_major) + '.' + str(f.header.version_minor))
    # print('Generation Software: ', f.header.software_id)
    # print('system_id: ', f.header.system_id)
    # print('Header Size: ', f.header.header_size)
    # print('file_global_encoding: ', f.header.global_encoding)
    # print('gps_time_type: ', f.header.gps_time_type)
    # print('guid: ', f.header.guid)
    print()

    # print('f.edge_flight_line: ', f.edge_flight_line)
    #print('f.return_num: ', f.return_num)
    # print('f.classification: ', f.classification)
    # print('f.scan_angle_rank: ', f.scan_angle_rank)
    # print('f.scan_dir_flag: ', f.scan_dir_flag)
    #print('f.num_returns: ', f.num_returns)
    # print('pt_src_id: ', f.pt_src_id)

    f.close()


if __name__ == "__main__":
    main()
