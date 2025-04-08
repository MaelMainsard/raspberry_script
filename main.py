from peewee import *
from models import NodeParam,NodeData
import datetime
import paho.mqtt.publish as publish

db = SqliteDatabase('./db/zigbee.db')

def manage_node():
    count = NodeParam.select().where(NodeParam.name == "esp32 room 1").count()

    if count > 0:
        existing_node = NodeParam.select().where(NodeParam.name == "esp32 room 1").get()
        existing_node.updated_at = datetime.datetime.now()
        existing_node.save()
        return existing_node
    else:
        new_node = NodeParam.create(name='esp32 room 1')
        return new_node
def get_data_to_send(node, data):
    new_temp = data["temp"]
    new_hum = data["hum"]

    query = (NodeData.select(
        fn.COUNT(NodeData.id).alias('count'),
        fn.SUM(NodeData.temperature).alias('temperature'),
        fn.SUM(NodeData.humidity).alias('humidity'),
    )
    .where(NodeData.node_id == node.id))

    result = query.get()

    if result.count > 0:
        total_count = result.count + 1
        avg_temperature = round((result.temperature + new_temp) / total_count, 1)
        avg_humidity = round((result.humidity + new_hum) / total_count, 1)
    else:
        avg_temperature = round(new_temp, 1)
        avg_humidity = round(new_hum, 1)

    return {
        "temperature": avg_temperature,
        "humidity": avg_humidity
    }
def save_data(node, temp, hum):
    NodeData.create(node_id=node.id, temperature=temp, humidity=hum)
def format_payload(node,data):
    payload = {
        "node_id": str(node.id),
        "node_name": node.name,
        "data": data,
    }
    return str(payload)

def main():
    db.connect()
    db.create_tables([NodeParam, NodeData], safe=True)

    my_node = manage_node()
    new_data = {
        "temp": 23.6,
        "hum": 56.3
    }

    data_to_send = get_data_to_send(my_node, new_data)

    print(f"Payload: {format_payload(my_node,data_to_send)}")

    # save_data(my_node, 23.6, 56.3)
    # publish.single("paho/test/topic", "payload", hostname="mqtt.eclipseprojects.io")


if __name__ == '__main__':
    main()