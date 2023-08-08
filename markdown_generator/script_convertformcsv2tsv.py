import csv

with open('Exported_Items.csv', 'r') as csv_file, open('output.tsv', 'w') as tsv_file:
    csv_reader = csv.DictReader(csv_file)
    tsv_writer = csv.writer(tsv_file, delimiter='\t')
    tsv_writer.writerow(['pub_date', 'title', 'venue',
                        'excerpt', 'citation', 'url_slug', 'paper_url'])
    for row in csv_reader:
        tsv_writer.writerow([row['Publication Year'], row['Title'], row['Publication Title'],
                            row['Abstract Note'], row['DOI'], row['Url'], row['Url']])
