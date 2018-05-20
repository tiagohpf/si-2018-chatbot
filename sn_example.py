# Redes semanticas
# -- Exemplo
# 
# Introducao a Inteligencia Artificial
# DETI / UA
#
# (c) Luis Seabra Lopes, 2012-2014
# 2014/10/15
#


from semantic_network import *

a = Association('socrates','professor','filosofia')
s = Subtype('homem','mamifero')
m = Member('socrates','homem')

da = Declaration('descartes',a)
ds = Declaration('darwin',s)
dm = Declaration('descartes',m)

z = SemanticNetwork()
z.insert(da)
z.insert(ds)
z.insert(dm)
z.insert(Declaration('darwin',Association('mamifero','mamar','sim')))
z.insert(Declaration('darwin',Association('homem','gosta','carne')))

# novas declaracoes

z.insert(Declaration('darwin',Subtype('mamifero','vertebrado')))
z.insert(Declaration('descartes', Member('aristoteles','homem')))

b = Association('socrates','professor','matematica')
z.insert(Declaration('descartes',b))
z.insert(Declaration('simao',b))
z.insert(Declaration('simoes',b))

z.insert(Declaration('descartes', Member('platao','homem')))

e = Association('platao','professor','filosofia')
z.insert(Declaration('descartes',e))
z.insert(Declaration('simao',e))

z.insert(Declaration('descartes',Association('mamifero','altura',1.2)))
z.insert(Declaration('descartes',Association('homem','altura',1.75)))
z.insert(Declaration('simao',Association('homem','altura',1.85)))
z.insert(Declaration('darwin',Association('homem','altura',1.75)))

z.insert(Declaration('descartes', Association('socrates','peso',80)))
z.insert(Declaration('darwin', Association('socrates','peso',75)))
z.insert(Declaration('darwin', Association('platao','peso',75)))


z.insert(Declaration('damasio', Association('filosofo','gosta','filosofia')))
z.insert(Declaration('damasio', Member('socrates','filosofo')))


# Extra - descomentar as restantes declaracoes para o exercicio 3.

z.insert(Declaration('descartes', AssocNum('socrates','pulsacao',51)))
z.insert(Declaration('darwin', AssocNum('socrates','pulsacao',61)))
z.insert(Declaration('darwin', AssocNum('platao','pulsacao',65)))

z.insert(Declaration('descartes',AssocNum('homem','temperatura',36.8)))
z.insert(Declaration('simao',AssocNum('homem','temperatura',37.0)))
z.insert(Declaration('darwin',AssocNum('homem','temperatura',37.1)))
z.insert(Declaration('descartes',AssocNum('mamifero','temperatura',39.0)))

z.insert(Declaration('simao',Association('homem','gosta','carne')))
z.insert(Declaration('darwin',Association('homem','gosta','peixe')))
z.insert(Declaration('simao',Association('homem','gosta','peixe')))
z.insert(Declaration('simao',Association('homem','gosta','couves')))

z.insert(Declaration('damasio', AssocOne('socrates','pai','sofronisco')))
z.insert(Declaration('darwin', AssocOne('socrates','pai','pericles')))
z.insert(Declaration('descartes', AssocOne('socrates','pai','sofronisco')))


#print(z)

print("1.1 predecessor('vertebrado', 'socrates'):", z.predecessor('vertebrado', 'socrates'))
print("1.2 predecessor('vertebrado', 'mulher'):", z.predecessor('vertebrado', 'mulher'))
print("2.1 predecessor_path('vertebrado', 'socrates'):", z.predecessor_path('vertebrado', 'socrates'))
print("2.2 predecessor_path('vertebrado', 'mulher'):", z.predecessor_path('vertebrado', 'mulher'))
print("2.3 predecessor_path('vertebrado', 'mamifero'):", z.predecessor_path('vertebrado', 'mamifero'))
print("3. associations():", z.associations())
print("4. instances():", z.instances())
print("5. interlocutores():", z.interlocutores())
print("6. types():", z.types())
print("7. entityAssociation('socrates'):", z.entityAssociations('socrates'))
print("8.1 userDeclarations('simao'):", z.userDeclarations('simao'))
print("8.2 userDeclarations('socrates'):", z.userDeclarations('socrates'))
print("9.1 numAssociations('simao'):", z.numAssociations('simao'))
print("9.2 numAssociations('socrates'):", z.numAssociations('socrates'))
print("10. entityAssociations('homem'):", z.entityAssociations('homem'))
print("11.1 a). query('socrates', 'gosta'):", z.query('socrates', 'gosta'))
print("11.2 a). query('platao', 'mamar'):", z.query('platao', 'mamar'))
print("11 b). query2('socrates', 'altura'):", z.query2('socrates', 'altura'))
print("12. query_cancel('socrates', 'altura'):", z.query_cancel('socrates', 'altura'))
print("13.1 query_assoc_value('socrates', 'peso'):", z.query_assoc_value('socrates', 'peso'))
print("13.2 query_assoc_value('homem', 'altura'):", z.query_assoc_value('homem', 'altura'))
print("14. query_down('mamifero', 'peso'):", z.query_down('mamifero', 'peso'))
print("15. query_induce('mamifero', 'altura):",z.query_induce('mamifero', 'altura'))
print("16.1 b) z.query_local_assoc('socrates', 'pai')", z.query_local_assoc('socrates', 'pai'))
print("16.2 b) z.query_local_assoc('socrates', 'pulsacao')", z.query_local_assoc('socrates', 'pulsacao'))
print("16.3 b) z.query_local_assoc('homem', 'gosta')", z.query_local_assoc('homem', 'gosta'))
