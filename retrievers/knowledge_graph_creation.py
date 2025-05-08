from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load credentials
load_dotenv()
URI = os.getenv("NEO4J_URL")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(URI, auth=(username, password))

def push_event_triplet(tx, person, event, date):
    """
    Creates nodes and relationships:
    (Person)-[:PARTICIPATED_IN]->(Event)-[:OCCURRED_ON]->(Date)
    """
    query = """
    MERGE (p:Person {name: $person})
    MERGE (e:Event {name: $event})
    MERGE (d:Date {value: $date})

    MERGE (p)-[:PARTICIPATED_IN]->(e)
    MERGE (e)-[:OCCURRED_ON]->(d)
    """
    tx.run(query, person=person, event=event, date=date)

def insert_event_triplets(triplets):
    """
    Insert a list of triplets where each is (person, event, date).
    """
    with driver.session() as session:
        for person, event, date in triplets:
            session.write_transaction(push_event_triplet, person, event, date)

# Example usage
triplets = [
    ("Prithvi Narayan Shah", "Unification of Nepal", "1768"),
    ("East India Company", "Sugauli Treaty", "1815"),
    ("Bahadur Shah", "Expansion Campaign", "1775"),
    ("King Birendra", "Born", "1945-12-28"),
    ("King Birendra", "Studied at Eton College", "1959"),
    ("King Birendra", "Studied at Harvard University", "1967"),
    ("King Birendra", "Married Aishwarya Rajya Laxmi Devi Shah", "1970-02-27"),
    ("King Birendra", "Became King of Nepal", "1972-01-31"),
    ("King Birendra", "Fathered Dipendra Bir Bikram Shah", "1971"),
    ("King Birendra", "Proclaimed Nepal a Zone of Peace", "1975"),
    ("King Birendra", "Faced People’s Movement for Democracy", "1990"),
    ("King Birendra", "Agreed to Constitutional Monarchy", "1990"),
    ("King Birendra", "Attended SAARC Summits", "1985"),  # representative event
    ("King Birendra", "Killed in Royal Palace Massacre", "2001-06-01"),
    ("Prithvi Narayan Shah", "Born", "1723"),
    ("Prithvi Narayan Shah", "Became King of Gorkha", "1743"),
    ("Prithvi Narayan Shah", "Married Narendra Rajya Lakshmi Devi", "1740s"),
    ("Prithvi Narayan Shah", "Fathered Pratap Singh Shah", "1751"),
    ("Prithvi Narayan Shah", "Captured Nuwakot", "1744"),
    ("Prithvi Narayan Shah", "Captured Kirtipur", "1767"),
    ("Prithvi Narayan Shah", "Captured Kathmandu", "1768"),
    ("Prithvi Narayan Shah", "Captured Patan", "1768"),
    ("Prithvi Narayan Shah", "Captured Bhaktapur", "1769"),
    ("Prithvi Narayan Shah", "Conquered Kirat region", "1772"),
    ("Prithvi Narayan Shah", "Died", "1775"),
    ("Pratap Singh Shah", "Born", "1751"),
    ("Pratap Singh Shah", "Became King of Nepal", "1775"),
    ("Pratap Singh Shah", "Married Rajendra Rajya Lakshmi Devi", "1770s"),
    ("Pratap Singh Shah", "Fathered Rana Bahadur Shah", "1775"),
    ("Pratap Singh Shah", "Died", "1777"),
    ("Rana Bahadur Shah", "Born", "1775"),
    ("Rana Bahadur Shah", "Became King of Nepal", "1777"),
    ("Rana Bahadur Shah", "Married Kantavati Devi", "1790s"),
    ("Rana Bahadur Shah", "Fathered Girvan Yuddha Bikram Shah", "1797"),
    ("Rana Bahadur Shah", "Abdicated Throne", "1799"),
    ("Rana Bahadur Shah", "Assassinated", "1806"),
    ("Girvan Yuddha Bikram Shah", "Born", "1797"),
    ("Girvan Yuddha Bikram Shah", "Became King of Nepal", "1799"),
    ("Girvan Yuddha Bikram Shah", "Anglo-Nepal War", "1814"),
    ("Girvan Yuddha Bikram Shah", "Died", "1816"),
    ("Rajendra Bikram Shah", "Born", "1813"),
    ("Rajendra Bikram Shah", "Became King of Nepal", "1816"),
    ("Rajendra Bikram Shah", "Married Samrajya Lakshmi Devi", "1830s"),
    ("Rajendra Bikram Shah", "Fathered Surendra Bikram Shah", "1829"),
    ("Rajendra Bikram Shah", "Abdicated Throne", "1847"),
    ("Rajendra Bikram Shah", "Died", "1881"),
    ("Surendra Bikram Shah", "Born", "1829"),
    ("Surendra Bikram Shah", "Became King of Nepal", "1847"),
    ("Surendra Bikram Shah", "Married Trailokya Rajya Lakshmi Devi", "1850s"),
    ("Surendra Bikram Shah", "Fathered Prithvi Bir Bikram Shah", "1875"),
    ("Surendra Bikram Shah", "Died", "1881"),
    ("Prithvi Bir Bikram Shah", "Born", "1875"),
    ("Prithvi Bir Bikram Shah", "Became King of Nepal", "1881"),
    ("Prithvi Bir Bikram Shah", "Married Divyeshwari Lakshmi Devi", "1890s"),
    ("Prithvi Bir Bikram Shah", "Fathered Tribhuvan Bir Bikram Shah", "1906"),
    ("Prithvi Bir Bikram Shah", "Died", "1911"),
    ("Tribhuvan Bir Bikram Shah", "Born", "1906"),
    ("Tribhuvan Bir Bikram Shah", "Became King of Nepal", "1911"),
    ("Tribhuvan Bir Bikram Shah", "Married Kanti Rajya Lakshmi Devi", "1920s"),
    ("Tribhuvan Bir Bikram Shah", "Fathered Mahendra Bir Bikram Shah", "1920"),
    ("Tribhuvan Bir Bikram Shah", "Went into Exile", "1950"),
    ("Tribhuvan Bir Bikram Shah", "Returned from Exile", "1951"),
    ("Tribhuvan Bir Bikram Shah", "Died", "1955"),
    ("Mahendra Bir Bikram Shah", "Born", "1920"),
    ("Mahendra Bir Bikram Shah", "Became King of Nepal", "1955"),
    ("Mahendra Bir Bikram Shah", "Married Indra Rajya Lakshmi Devi", "1940s"),
    ("Mahendra Bir Bikram Shah", "Fathered Birendra Bir Bikram Shah", "1945"),
    ("Mahendra Bir Bikram Shah", "Died", "1972"),
    ("Birendra Bir Bikram Shah", "Born", "1945"),
    ("Birendra Bir Bikram Shah", "Became King of Nepal", "1972"),
    ("Birendra Bir Bikram Shah", "Married Aishwarya Rajya Laxmi Devi Shah", "1970s"),
    ("Birendra Bir Bikram Shah", "Fathered Dipendra Bir Bikram Shah", "1971"),
    ("Birendra Bir Bikram Shah", "Died", "2001"),
    ("Dipendra Bir Bikram Shah", "Born", "1971"),
    ("Dipendra Bir Bikram Shah", "Became King of Nepal", "2001"),
    ("Dipendra Bir Bikram Shah", "Died", "2001"),
    ("Gyanendra Bir Bikram Shah", "Born", "1947"),
    ("Gyanendra Bir Bikram Shah", "Became King of Nepal (First Reign)", "1950"),
    ("Gyanendra Bir Bikram Shah", "Stepped Down", "1951"),
    ("Gyanendra Bir Bikram Shah", "Became King of Nepal (Second Reign)", "2001"),
    ("Gyanendra Bir Bikram Shah", "Married Komal Rajya Lakshmi Devi", "1970"),
    ("Gyanendra Bir Bikram Shah", "Fathered Paras Shah", "1971"),
    ("Gyanendra Bir Bikram Shah", "Monarchy Abolished", "2008"),
    ("King Mahendra", "Dissolved democratic government and imposed Panchayat system", "1960-12-15"),
    ("King Mahendra", "Promulgated new constitution establishing Panchayat system", "1962-12-16"),
    ("King Birendra", "Held national referendum on Panchayat system", "1980"),
    ("King Birendra", "Reinstated multiparty democracy after People's Movement", "1990-04-08"),
    ("King Birendra", "Promulgated new constitution establishing constitutional monarchy", "1990-11-09"),
    ("King Birendra", "Faced Maoist Insurgency", "1996"),
    ("King Birendra", "Declared Nepal a Zone of Peace", "1975"),
    ("King Birendra", "Attended SAARC Summits", "1985"),  # representative event
    ("King Birendra", "Killed in Royal Palace Massacre", "2001-06-01"),
    ("King Gyanendra", "Became King of Nepal (First Reign)", "1950"),
    ("King Gyanendra", "Stepped Down", "1951"),
    ("King Gyanendra", "Became King of Nepal (Second Reign)", "2001"),
    ("King Gyanendra", "Married Komal Rajya Lakshmi Devi", "1970"),
    ("King Gyanendra", "Fathered Paras Shah", "1971"),
    ("King Gyanendra", "Monarchy Abolished", "2008"),
    ("King Gyanendra", "Faced People's Movement for Democracy", "2006"),
    ("King Gyanendra", "Agreed to Constitutional Monarchy", "2006"),
    ("King Gyanendra", "Faced Maoist Insurgency", "1996"),
    ("King Gyanendra", "Declared Nepal a Zone of Peace", "1975"),
    ("King Gyanendra", "Attended SAARC Summits", "1985"),  # representative event
    ("Communist Party of Nepal (Maoist)", "Launched armed insurgency (People's War)", "1996-02-13"),
    ("Government of Nepal", "Declared state of emergency", "2001-11"),
    ("Government of Nepal and Maoists", "Signed Comprehensive Peace Accord", "2006-11-21"),
    ("Jung Bahadur Rana", "Became Prime Minister", "1846-09-15"),
    ("Bam Bahadur Kunwar", "Became Prime Minister", "1856-08-01"),
    ("Ranodip Singh Kunwar", "Became Prime Minister", "1877-02-25"),
    ("Bir Shumsher Jung Bahadur Rana", "Became Prime Minister", "1885-11-22"),
    ("Dev Shumsher Jung Bahadur Rana", "Became Prime Minister", "1901-03-05"),
    ("Chandra Shumsher Jung Bahadur Rana", "Became Prime Minister", "1901-06-27"),
    ("Bhim Shumsher Jung Bahadur Rana", "Became Prime Minister", "1929-11-26"),
    ("Juddha Shumsher Jung Bahadur Rana", "Became Prime Minister", "1932-09-01"),
    ("Padma Shumsher Jung Bahadur Rana", "Became Prime Minister", "1945-11-29"),
    ("Mohan Shumsher Jung Bahadur Rana", "Became Prime Minister", "1948-04-30"),
    ("Nepal", "Abolished monarchy and declared republic", "2008-05-28"),
    ("Matrika Prasad Koirala", "Became Prime Minister", "1951-11-16"),
    ("Tanka Prasad Acharya", "Became Prime Minister", "1956-01-27"),
    ("Subarna Shamsher Rana", "Became Prime Minister", "1958-05-27"),
    ("Bishweshwar Prasad Koirala", "Became Prime Minister", "1959-05-27"),
    ("Tulsi Giri", "Became Prime Minister", "1960-12-15"),
    ("Surya Bahadur Thapa", "Became Prime Minister", "1963-04-05"),
    ("Nagendra Prasad Rijal", "Became Prime Minister", "1973-07-16"),
    ("Lokendra Bahadur Chand", "Became Prime Minister", "1983-07-12"),
    ("Marich Man Singh Shrestha", "Became Prime Minister", "1986-06-15"),
    ("Krishna Prasad Bhattarai", "Became Prime Minister", "1990-04-19"),
    ("Girija Prasad Koirala", "Became Prime Minister", "1991-05-26"),
    ("Man Mohan Adhikari", "Became Prime Minister", "1994-11-30"),
    ("Sher Bahadur Deuba", "Became Prime Minister", "1995-09-12"),
    ("Pushpa Kamal Dahal", "Became Prime Minister", "2008-08-18"),
    ("Madhav Kumar Nepal", "Became Prime Minister", "2009-05-25"),
    ("Jhala Nath Khanal", "Became Prime Minister", "2011-02-03"),
    ("Baburam Bhattarai", "Became Prime Minister", "2011-08-29"),
    ("Khadga Prasad Sharma Oli", "Became Prime Minister", "2015-10-11"),
    ("Sher Bahadur Deuba", "Became Prime Minister", "2017-06-07"),
    ("Khadga Prasad Sharma Oli", "Became Prime Minister", "2018-02-15"),
    ("Sher Bahadur Deuba", "Became Prime Minister", "2021-07-13"),
    ("Pushpa Kamal Dahal", "Became Prime Minister", "2022-12-26"),
    ("Pushpa Kamal Dahal", "Became Prime Minister", "2023-06-04"),
    ("BP Koirala", "Born in Varanasi, British India", "1914-09-08"),
    ("BP Koirala", "Married Sushila Koirala", "1936"),
    ("BP Koirala", "Fathered Prakash Koirala", "1941"),
    ("BP Koirala", "Fathered Shashanka Koirala", "1945"),
    ("BP Koirala", "Fathered Shree Harsha Koirala", "1947"),
    ("BP Koirala", "Fathered Chetana Koirala", "1949"),
    ("BP Koirala", "Completed Bachelor's degree in Economics and Politics from Banaras Hindu University", "1934"),
    ("BP Koirala", "Earned Law degree from University of Calcutta", "1937"),
    ("BP Koirala", "Joined Indian National Congress", "1934"),
    ("BP Koirala", "Founded Nepal National Congress", "1947"),
    ("BP Koirala", "Merged Nepal National Congress into Nepali Congress", "1950"),
    ("BP Koirala", "Appointed Minister of Home Affairs of Nepal", "1951-02-21"),
    ("BP Koirala", "Became Prime Minister of Nepal", "1959-05-27"),
    ("BP Koirala", "Imprisoned after royal coup by King Mahendra", "1960-12-15"),
    ("BP Koirala", "Released from prison", "1968"),
    ("BP Koirala", "Went into exile in India", "1968"),
    ("BP Koirala", "Returned to Nepal", "1976"),
    ("BP Koirala", "Died in Kathmandu, Nepal", "1982-07-21"),
    ("Madan Bhandari", "Born in Dhungesangu, Taplejung, Nepal", "1951-06-27"),
    ("Madan Bhandari", "Married Bidya Devi Bhandari", "1982"),
    ("Madan Bhandari", "Fathered Usha Kiran Bhandari", "1983"),
    ("Madan Bhandari", "Fathered Nisha Kusum Bhandari", "1985"),
    ("Madan Bhandari", "Completed Master's degrees in Political Science and Nepali Literature from Banaras Hindu University", "1975"),
    ("Madan Bhandari", "Joined Janabadi Sanskritik Morcha", "1972"),
    ("Madan Bhandari", "Founded Mukti Morcha Samuha", "1976"),
    ("Madan Bhandari", "Became General Secretary of Communist Party of Nepal (Marxist-Leninist)", "1986"),
    ("Madan Bhandari", "Merged party to form Communist Party of Nepal (Unified Marxist-Leninist)", "1991"),
    ("Madan Bhandari", "Developed People's Multiparty Democracy ideology", "1991"),
    ("Madan Bhandari", "Elected to Parliament defeating Krishna Prasad Bhattarai", "1991"),
    ("Madan Bhandari", "Died in a car accident in Dasdhunga, Chitwan", "1993-05-16"),
    ("Manadeva I", "Born", "464 CE"),
    ("Manadeva I", "Ascended to the throne", "464 CE"),
    ("Manadeva I", "Expanded the kingdom east and west", "464–505 CE"),
    ("Manadeva I", "Issued first dated stone inscription in Nepal", "464 CE"),
    ("Manadeva I", "Died", "505 CE"),

    ("Amshuverma", "Born", "605 CE"),
    ("Amshuverma", "Became Prime Minister", "605 CE"),
    ("Amshuverma", "Assumed kingship", "605 CE"),
    ("Amshuverma", "Promoted Buddhism and constructed monasteries", "605–621 CE"),
    ("Amshuverma", "Established diplomatic relations with Tibet, China, and India", "605–621 CE"),
    ("Amshuverma", "Died", "621 CE"),

    ("Narendradeva", "Born", "640 CE"),
    ("Narendradeva", "Restored to the throne with Tibetan support", "643 CE"),
    ("Narendradeva", "Reigned during a period of peace and prosperity", "643–679 CE"),
    ("Narendradeva", "Died", "679 CE"),
    ("Arideva Malla", "Founded Malla dynasty", "1201 CE"),
    ("Jayasthiti Malla", "Unified Kathmandu Valley under single rule", "1382 CE"),
    ("Jayasthiti Malla", "Introduced legal and social code based on Hindu principles", "1382–1395 CE"),
    ("Yaksha Malla", "Divided the kingdom among his sons", "1482 CE"),
    ("Pratap Malla", "Promoted arts and culture in Kathmandu", "1641–1674 CE"),
    ("Siddhi Narasimha Malla", "Developed Lalitpur as a center of art and architecture", "1620–1661 CE"),
    ("Bhupatindra Malla", "Commissioned Nyatapola Temple in Bhaktapur", "1702 CE"),
    ("Ranajit Malla", "Last Malla king of Bhaktapur", "1722–1769 CE"),
    ("Ranajit Malla", "Defeated by Prithvi Narayan Shah", "1769 CE"),
    ("Lakhan Thapa Magar", "Led rebellion against Jung Bahadur Rana's authority", "1877-02-14"),
    ("Nepal Praja Parishad", "Founded by Dashrath Chand and Tanka Prasad Acharya", "1936-06-04"),
    ("Dashrath Chand", "Executed by Rana regime", "1941-01"),
    ("Gangalal Shrestha", "Executed by Rana regime", "1941-01"),
    ("Dharma Bhakta Mathema", "Executed by Rana regime", "1941-01"),
    ("Shukraraj Shastri", "Executed by Rana regime", "1941-01"),
    ("Jayatu Sanskritam Movement", "Initiated by students demanding educational reforms", "1947-06-01"),
    ("Ram Prasad Neupane", "Led Jayatu Sanskritam Movement", "1947-06-01"),
    ("Nepali Congress", "Formed through merger of Nepali National Congress and Nepal Democratic Congress", "1950"),
    ("Nepali Congress", "Launched armed revolution against Rana regime", "1950-11"),
    ("Tribhuvan Bir Bikram Shah", "Fled to India seeking support against Rana regime", "1950-11-10"),
    ("Tribhuvan Bir Bikram Shah", "Returned to Nepal and reinstated as monarch", "1951-02-15"),
    ("Delhi Compromise", "Agreement among King Tribhuvan, Rana regime, and Nepali Congress", "1951-02-07"),
    ("Mohan Shumsher Jung Bahadur Rana", "Resigned as Prime Minister", "1951-03-13"),
    ("BP Koirala", "Appointed Prime Minister of Nepal", "1959-05-27"),



]









insert_event_triplets(triplets)

driver.close()
