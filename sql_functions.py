#! /usr/bin/env

import sys, sqlite3, os




def database_connect():
    database="ensembl_hs63_simple.sqlite"
    current_path=os.path.dirname(__file__)
    db=os.path.join(current_path ,database)
    # Database connection
    conn = sqlite3.connect(db)
    c=conn.cursor()
    return conn

def close_and_commit(conn):
    # Save (commit) the changes
    conn.commit()

    # We must close the connection if we are done with it.
    conn.close()


def request_organisms():
    # returns organism from ensembl_hs63_simple database
    conn=database_connect()
    c=conn.cursor()
    r=c.execute('SELECT DISTINCT Atlas_Organism_part FROM Expression ORDER BY Atlas_Organism_part ASC ')
    values=[]
    for tuple in r :
        if tuple[0]:
            values.append(tuple[0])
    close_and_commit(conn)

    return values

def request_genes_from_organism(part):
    # Returns genes for a given organism
    t=(part,)
    sql_compl="""
    SELECT DISTINCT GENES.ensembl_gene_id, GENES.associated_gene_name
    FROM EXPRESSION
    INNER JOIN TRANSCRIPTS ON EXPRESSION.Ensembl_Transcript_Id = TRANSCRIPTS.ENSEMBL_TRANSCRIPT_ID
    INNER JOIN GENES ON TRANSCRIPTS.ENSEMBL_GENE_ID = GENES.ENSEMBL_GENE_ID
    WHERE EXPRESSION.ATLAS_ORGANISM_PART=?
    ORDER BY Genes.ensembl_gene_id"""
    conn=database_connect()
    c=conn.cursor()
    c.execute(sql_compl, t)
    r=c.fetchall()
    values=[]
    for tuple in r :
        if tuple[0]:
            values.append(tuple)
    close_and_commit(conn)

    return values

def request_gene_info(id):
    t=(id,)
    columns=[ "Ensembl Gene ID", "Associated gene name", "Chromosome name", "Band", "Strand", "Gene Start", "Gene end", "Transcript Count"]
    sql_gene_info="""SELECT Ensembl_Gene_ID, associated_gene_name, Chromosome_name, Band, Strand, Gene_Start, Gene_end, Transcript_Count
    FROM GENES
    WHERE GENES.ENSEMBL_GENE_ID=?"""
    conn=database_connect()
    c=conn.cursor()
    c.execute(sql_gene_info, t)
    r=c.fetchall()
    values=list(zip(columns, [str(info) for info in r[0]]))
    # for i in values :
    #     print(str(i[0]) + str(i[1]))
    close_and_commit(conn)
    return values


def request_geneRelated_organisms():
    t = (id, )
    Atlas = []
    sql_compl="""SELECT atlas_organism_part, Count(ensembl_transcript_id)
    FROM Transcripts
    NATURAL JOIN Expression
    WHERE ensembl_gene_id = ? AND atlas_organism_part IS NOT NULL
    GROUP BY atlas_organism_part
    ORDER BY atlas_organism_part DESC
    """
    conn=database_connect()
    c=conn.cursor()
    c.execute(sql_compl, t)
    r=c.fetchall()
    for geneInfo in r:
        if None not in geneInfo:
            Atlas.append(geneInfo)

            close_and_commit(conn)
            return Atlas

def request_transcripts_from_gene(id):
    t = (id, )
    transcripts = []
    sql_compl="""SELECT ensembl_transcript_id
    FROM Transcripts
    WHERE ensembl_gene_id = ?
    """
    conn=database_connect()
    c=conn.cursor()
    c.execute(sql_compl, t)
    r=c.fetchall()
    for geneInfo in r:
        if None not in geneInfo:
            transcripts.append(geneInfo)

    close_and_commit(conn)
    return transcripts

def request_transcripts_info(id):
    t = (id, )
    sql_compl="""SELECT T.ensembl_transcript_id, Transcript_start, Transcript_end
    FROM Transcripts T NATURAL JOIN Genes G
    WHERE ensembl_gene_id = ?
    """
    conn=database_connect()
    c=conn.cursor()
    c.execute(sql_compl, t)
    r=c.fetchall()
    info=[]
    for geneInfo in r:
        if None not in geneInfo:
            info.append(geneInfo)
    close_and_commit(conn)
    return info


def request_transcript_count(id):
    t = (id, )
    Atlas = []
    # sql_compl="""SELECT E.atlas_organism_part, E.ensembl_transcript_id
    # FROM Transcripts T NATURAL JOIN Expression E
    # WHERE ensembl_gene_id = ? AND E.Atlas_Organism_Part IS NOT NULL
    # ORDER BY ATLAS_ORGANISM_PART ASC"""

    sql_compl="""SELECT E.atlas_organism_part, count(E.ensembl_transcript_id) as C
    FROM Transcripts T NATURAL JOIN Expression E
    WHERE ensembl_gene_id = ? AND E.Atlas_Organism_Part IS NOT NULL
    GROUP BY ATLAS_ORGANISM_PART
    ORDER BY ATLAS_ORGANISM_PART ASC, C Desc
    """
    conn=database_connect()
    c=conn.cursor()
    c.execute(sql_compl, t)
    r=c.fetchall()
    for geneInfo in r:
        if None not in geneInfo:
            Atlas.append(geneInfo)
    close_and_commit(conn)

    return Atlas
