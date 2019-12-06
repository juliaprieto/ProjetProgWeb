#! /usr/bin/env python3

from flask import Flask
import flask as fk
import os
from io import BytesIO
from sql_functions import request_organisms, request_genes_from_organism, request_gene_info, request_transcript_count, request_transcripts_from_gene, request_transcripts_info
import matplotlib.pyplot as plt
app=Flask(__name__)



@app.route("/")
def root():
    values=request_organisms()
    return fk.render_template("atlas.html", atlas=values)


@app.route("/parts/<part>/genes", methods=['GET'])
def links(part):
    values=request_genes_from_organism(part)
    return fk.render_template("genes.html", genes=values, organism=part)


@app.route("/genes/<id>/transcripts.svg")
def transcripts(id):
    t_info=request_transcripts_info(id)
    g_info=request_gene_info(id)
    h=len(t_info)
    gene_pos= (int(g_info[5][1]), int(g_info[6][1]))
    gene_len= int(g_info[6][1]) - int(g_info[5][1])
    t_coord = []
    y=5
    for t in t_info:
        start=int(t[1])
        end=int(t[2])
        x= 10 + (start-gene_pos[0])* 280 / gene_len
        X = ((end-start)*280 / gene_len)
        print(x)
        t_coord.append((t[0], int(x), int(X) , int(y)))
        y+= 8


    return fk.render_template("ensembl_transcript.html", t_info=t_info,t_coord=t_coord, g_info=g_info, gene_id=id, h=len(t_info)*8 + 10)

@app.route("/image/<gene_id>")
def graph(gene_id):

    Atlas=request_transcript_count(gene_id)

    labels=[]
    values=[]
    for tup in Atlas :
        print(tup)
        labels.append(tup[0])
        values.append(tup[1])
    print(labels)
    fig, (ax) = plt.subplots(1, 1)
    ax.bar(labels,values)
    plt.suptitle(f"Distribution of {gene_id} transcripts in organisms")
    plt.xticks(rotation=90)
    b = BytesIO()
    fig.savefig(b, format="png",bbox_inches='tight')

    # To render html with image only
    # resp = fk.make_response(b.getvalue())
    # resp.headers['content-type'] = 'image/png'
    # return resp
    return b.getvalue()

@app.route("/genes/<id>/parts.png")
def hist(id):

    return fk.render_template("gene_expression.html", gene_id=id)

@app.route("/genes/<id>")
def gene_info(id):
    values=request_gene_info(id)
    return fk.render_template("fiche_gene.html", gene=values )
