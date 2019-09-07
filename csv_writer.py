import csv


field_names = ["Pub date", "Pub time", "Title", "Article text", "Comment Number"]


def csv_write(collected_items):
    with open("output.csv", "w", encoding='utf-8') as f:
        writer = csv.DictWriter(f, field_names)

        writer.writerow({x: x for x in field_names})

        for item_property_dict in collected_items:
            writer.writerow(item_property_dict)
