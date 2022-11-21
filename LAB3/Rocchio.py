from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
import argparse
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import Q
from elasticsearch.client import CatClient
import numpy as np
import operator


def document_term_vector(client, index, id):
    """
    Returns the term vector of a document and its statistics a two sorted list of pairs (word, count)
    The first one is the frequency of the term in the document, the second one is the number of documents
    that contain the term

    :param client:
    :param index:
    :param id:
    :return:
    """
    termvector = client.termvectors(index=index, id=id, fields=['text'],
                                    positions=False, term_statistics=True)

    file_td = {}
    file_df = {}

    if 'text' in termvector['term_vectors']:
        for t in termvector['term_vectors']['text']['terms']:
            file_td[t] = termvector['term_vectors']['text']['terms'][t]['term_freq']
            file_df[t] = termvector['term_vectors']['text']['terms'][t]['doc_freq']
    return sorted(file_td.items()), sorted(file_df.items())


def toTFIDF(client, index, file_id):
    """
    Returns the term weights of a document

    :param file:
    :return:
    """

    # Get the frequency of the term in the document, and the number of documents
    # that contain the term
    file_tv, file_df = document_term_vector(client, index, file_id)

    max_freq = max([f for _, f in file_tv])

    dcount = doc_count(client, index)

    tfidfw = {}
    for (t, w), (_, df) in zip(file_tv, file_df):
        tf = w/max_freq
        idf = np.log2(dcount/df)
        tfidfw[t] = tf*idf
    return tfidfw


def doc_count(client, index):
    """
    Returns the number of documents in an index

    :param client:
    :param index:
    :return:
    """
    return int(CatClient(client).count(index=[index], format='json')[0]['count'])


def querydict(query):
    queryDict = {}
    for t in query:
        if '^' in t:
            term, weight = t.split('^')
            weight = float(weight)
        else:
            term = t
            weight = 1.0
        queryDict[term] = weight
    return queryDict


def dictquery(dictionary):
    dictQuery = []
    for (term, weight) in dictionary:
        dictQuery.append(term + '^' + str(weight))
    return dictQuery


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, help='Index to search')
    parser.add_argument('--nrounds', type=int, help='Number times to execute Rocchio')
    parser.add_argument('--k', type=int, help='Number of relevant documents')
    parser.add_argument('--r', type=int, help='Number of relevant terms')
    parser.add_argument('--query', default=None, nargs=argparse.REMAINDER, help='List of words to search')

    args = parser.parse_args()

    index = args.index
    nrounds = args.nrounds
    r = args.r
    query = args.query

    print(query)
    k = args.k

    alpha = 1
    beta = 0.5
    try:
        client = Elasticsearch()
        s = Search(using=client, index=index)
        if query is not None:
            for nr in range(0,nrounds):
                q = Q('query_string',query=query[0])
                for i in range(1, len(query)):
                    q &= Q('query_string',query=query[i])
                s = s.query(q)
                response = s[0:k].execute()

                queryDict = querydict(query)

                docComp = {}
                print(f"{response.hits.total['value']} Documents")

                for res in response:
                    file_tw = toTFIDF(client, index, res.meta.id)
                    docComp = {t: docComp.get(t, 0) + file_tw.get(t, 0)
                               for t in set(file_tw) | set(docComp)}

                betaDocs = {t: beta*docComp.get(t, 0)/k for t in set(docComp)}
                preQuery = {t: alpha*queryDict.get(t, 0) for t in set(queryDict)}
                postQuery = {t: betaDocs.get(t, 0) + preQuery.get(t, 0) for t in set(preQuery)|set(betaDocs)}

                postQuery = sorted(postQuery.items(), key= operator.itemgetter(1), reverse=True)
                postQuery = postQuery[:r]

                query = dictquery(postQuery)
                print(query)

            """
            for res in response:  # only returns a specific number of results
                print(f'ID= {res.meta.id} SCORE={res.meta.score}')
                print(f'PATH= {res.path}')
                print(f'TEXT: {res.text[:50]}')
                print('-----------------------------------------------------------------')
            """

        else:
            print('No query parameters passed')

        print(f"{response.hits.total['value']} Documents")

    except NotFoundError:
        print(f'Index {index} does not exists')
