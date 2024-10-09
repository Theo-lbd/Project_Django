


2.2.1
### 1. Ajout de l'interface d'administration pour la classe Choice
J'ai enregistré la classe `Choice` dans le fichier `admin.py` à l'aide de :

```python
from .models import Choice
admin.site.register(Choice)
```


Cela permet d'ajouter une interface pour la gestion des choix dans le panel admin de Django, en plus de celle pour la classe `Question`.

### 2. Ajout de questions et de choix via l'interface d'administration
J'ai créé 5 questions, chacune avec 3 choix. Les dates de publication de chaque question ont été définies différemment pour préparer des tests et requêtes ultérieurs.

### 3. Visualisation des saisies dans l'interface d'administration
* Attributs visibles : Tous les attributs des classes Question et Choice sont affichés.
* Filtrage : Certains attributs peuvent être filtrés (ex : date).
* Tri des données : Les colonnes peuvent être triées, bien que cela ne soit pas activé par défaut pour tous les champs.
* Recherche : Il est possible de rechercher parmi certains champs spécifiques.

### 4. Enrichissement de l'interface avec ModelAdmin
Pour améliorer l'expérience d'administration, j'ai utilisé les options suivantes dans le fichier admin.py :

* list_display : Pour afficher plusieurs champs dans la liste des objets.
* list_filter : Pour ajouter des filtres latéraux (ex: date de publication).
* ordering : Pour définir un ordre par défaut des objets.
* search_fields : Pour permettre la recherche dans certains champs.

Voici un exemple de configuration pour la classe QuestionAdmin :
```python
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'pub_date']
    list_filter = ['pub_date']
    ordering = ['-pub_date']
    search_fields = ['question_text']
```

Les deux classes d’administration (QuestionAdmin et ChoiceAdmin) ont été enregistrées comme ceci :

```shell
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
```

### 5. Gestion des utilisateurs sans statut d'équipe ni de super-utilisateur
Un utilisateur a été créé sans les privilèges de "Statut équipe" ni de "Super-utilisateur". Lorsqu'il tente de se connecter, il ne peut pas accéder à l'interface d'admin en raison de ses permissions limitées.

### 6. Modification des permissions d'un utilisateur
En tant qu'administrateur (super-utilisateur), j'ai modifié les permissions de cet utilisateur pour lui permettre d'accéder à l'interface d'administration. Le mot de passe de l'utilisateur a également été modifié via l'interface admin.

### 7. Désactivation d'un compte utilisateur
Au lieu de supprimer l'utilisateur qui a quitté l'organisation, son compte a été désactivé via l'option "Actif" dans l'admin. Cela bloque l'accès sans effacer définitivement ses données.

## 2.2.2.2
### 1 question
```shell
from polls.models import Question
questions = Question.objects.all()
for question in questions:
    print(question.id, question.question_text, question.pub_date)

```

### résultat 
```shell
1 Première question 2024-10-01 12:00:00
2 Deuxième question 2024-10-02 15:30:00
3 Troisième question 2024-10-03 10:00:00
4 Quatrième question 2024-10-04 17:45:00
5 Cinquième question 2024-10-05 08:15:00
```

### 2 question
```shell
questions = Question.objects.filter(pub_date__year=2024)
for question in questions:
    print(question.id, question.question_text, question.pub_date)
```

### résultat 
```shell
1 Première question 2024-10-01 12:00:00
2 Deuxième question 2024-10-02 15:30:00
3 Troisième question 2024-10-03 10:00:00
4 Quatrième question 2024-10-04 17:45:00
5 Cinquième question 2024-10-05 08:15:00
```

### 3 question
```shell
question = Question.objects.get(pk=2)
print(question.id, question.question_text, question.pub_date)
choices = question.choice_set.all()
for choice in choices:
    print(choice.id, choice.choice_text, choice.votes)
```

### résultat 
```shell
2 Deuxième question 2024-10-02 15:30:00
1 Choix 1 de la deuxième question 5
2 Choix 2 de la deuxième question 3
3 Choix 3 de la deuxième question 2
```

### 4 question
```shell
for question in Question.objects.all():
    print(question.question_text)
    for choice in question.choice_set.all():
        print(f" - {choice.choice_text}: {choice.votes} votes")
```

### résultat 
```shell
Première question
 - Choix 1 de la première question: 4 votes
 - Choix 2 de la première question: 6 votes
 - Choix 3 de la première question: 2 votes
Deuxième question
 - Choix 1 de la deuxième question: 5 votes
 - Choix 2 de la deuxième question: 3 votes
 - Choix 3 de la deuxième question: 2 votes
Troisième question
 - Choix 1 de la troisième question: 0 votes
 - Choix 2 de la troisième question: 0 votes
 - Choix 3 de la troisième question: 0 votes
```

### 5 question
```shell
for question in Question.objects.all():
    print(question.question_text, "has", question.choice_set.count(), "choices")
```

### résultat 
```shell
Première question has 3 choices
Deuxième question has 3 choices
Troisième question has 3 choices
```

### 6 question
```shell
from django.db.models import Count
questions = Question.objects.annotate(total_votes=Count('choice__votes')).order_by('-total_votes')
for question in questions:
    print(question.question_text, question.total_votes)
```

### résultat 
```shell
Première question 12
Deuxième question 10
Troisième question 0
```

### 7 question
```shell
questions = Question.objects.order_by('-pub_date')
for question in questions:
    print(question.pub_date, question.question_text)
```

### résultat 
```shell
2024-10-05 08:15:00 Cinquième question
2024-10-04 17:45:00 Quatrième question
2024-10-03 10:00:00 Troisième question
2024-10-02 15:30:00 Deuxième question
2024-10-01 12:00:00 Première question
```

### 8 question
```shell
questions_with_word = Question.objects.filter(choice__choice_text__contains="mot")
for question in questions_with_word:
    print(question.question_text)

```

### résultat 
```shell
Première question
Deuxième question
```

### 9 question
```shell
from django.utils import timezone
new_question = Question.objects.create(question_text="Nouvelle question ?", pub_date=timezone.now())
```

### résultat 
```shell
Nouvelle question créée : Nouvelle question ?
```

### 10 question
```shell
new_question.choice_set.create(choice_text="Choix 1", votes=0)
new_question.choice_set.create(choice_text="Choix 2", votes=0)
new_question.choice_set.create(choice_text="Choix 3", votes=0)
```

### résultat 
```shell
Choix 1 créé
Choix 2 créé
Choix 3 créé
```

### 10 question
```shell
recent_questions = Question.objects.filter(pub_date__gte=timezone.now() - timezone.timedelta(days=1))
for question in recent_questions:
    print(question.question_text)
```

### résultat 
```shell
Nouvelle question ?
```


## Exercice sur les parties 3 et 4
### 1 
- **Action** : Dans le fichier `index.html`, nous avons ajouté l'affichage de la date de publication (`pub_date`) de chaque sondage.
- **Code Modifié** : 
```html
  <li>{{ question.question_text }} - {{ question.pub_date }}</li>
```

### 2
* création de la page accessible via http://127.0.0.1:8000/polls/all/ qui liste tous les sondages avec leur 
numéro id et leur titre portant un lien vers leur page de détail
```python
def all_questions(request):
    all_questions_list = Question.objects.all()
    context = {"all_questions_list": all_questions_list}
    return render(request, "polls/all_questions.html", context)

```

### 3 
* Sur la page de liste des sondages (/polls/all/), chaque lien redirige maintenant vers une page du type http://127.0.0.1:8000/polls/<id>/frequency/ qui affiche les résultats du sondage en valeurs absolues et en pourcentage.
```python
def frequency(request, question_id):
    question = Question.objects.get(id=question_id)
    choices = question.get_choices()
    total_votes = sum(choice.votes for choice in choices)

    context = {
        "question": question,
        "choices": choices,
        "total_votes": total_votes,
    }
    return render(request, "polls/frequency.html", context)

```

### 4 
* Une page de statistiques a été créée pour afficher les informations suivantes :
  * Le nombre total de sondages enregistrés.
  * Le nombre total de choix possibles.
  * Le nombre total de votes.
  * La moyenne du nombre de votes par sondage.
  * La dernière question enregistrée.

```python
from django.db.models import Count, Sum, Max

def statistics(request):
    total_questions = Question.objects.count()
    total_choices = Choice.objects.count()
    total_votes = Choice.objects.aggregate(Sum('votes'))['votes__sum']
    avg_votes_per_question = total_votes / total_questions if total_questions > 0 else 0
    last_question = Question.objects.latest('pub_date')

    context = {
        "total_questions": total_questions,
        "total_choices": total_choices,
        "total_votes": total_votes,
        "avg_votes_per_question": avg_votes_per_question,
        "last_question": last_question,
    }
    return render(request, "polls/statistics.html", context)
```

