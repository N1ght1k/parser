import xml.etree.ElementTree as ET
from parser import myconnutils
import traceback


def add_with_none(tag, text):
    if text is not None:
        info[tag] = text
    else:
        info[tag] = 'None'


def enum_reg_gate_items(number_of_items):
    for item in number_of_items:
        if number_of_items.tag in info:
            info[number_of_items.tag] += ', ' + str(item.attrib['caption'])
        else:
            add_with_none(number_of_items.tag, str(item.attrib['caption']))


def insert_in_table(table, columns, values):
    sql_query = 'INSERT INTO %s (%s) VALUES (%s);' % (table, columns, values)
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        connection.commit()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


def update_table(table, values, flight_id):
    sql_query = 'UPDATE %s SET %s WHERE flight_id = \'%s\';' % (table, values, flight_id)
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query)
        connection.commit()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())


def get_flight(flight_id, table):
    sql_query = 'SELECT flight FROM %s WHERE flight_id = \'%s\';' % (table, flight_id)
    cursor = connection.cursor()
    cursor.execute(sql_query)
    result = cursor.fetchone()
    return result


def parse_xml(path, xml_type):
    root = ET.parse(path).getroot()
    for block in root:
        is_exist = False
        for elem_in_block in block:
            if elem_in_block.tag == 'flight_id':
                add_with_none(elem_in_block.tag, elem_in_block.text)
                flight = get_flight(elem_in_block.text, xml_type)
                if flight is not None:
                    is_exist = True
            elif elem_in_block.tag == 'numbers_gate' or elem_in_block.tag == 'numbers_reg':
                enum_reg_gate_items(elem_in_block)
            elif elem_in_block.tag == 'airports':
                for airports in elem_in_block:
                    for airport_item in airports.attrib:
                        info[airport_item] = airports.attrib[airport_item]
            else:
                add_with_none(elem_in_block.tag, elem_in_block.text)
        print(info)
        if is_exist:
            a = []
            for key in info.keys():
                a.append('%s = \'%s\'' % (key, info[key]))
            items = ', '.join(a)
            print(items)
            update_table(xml_type, items, info['flight_id'])
        else:
            keys_for_sql = ', '.join(info.keys())
            values_for_sql = '\'' + '\', \''.join(info.values()) + '\''
            insert_in_table(xml_type, keys_for_sql, values_for_sql)
        info.clear()


info = {}
connection = myconnutils.get_connection()
print("Connect successful!")
parse_xml(r'***', 'departure')
parse_xml(r'***', 'arrival')
connection.close()
