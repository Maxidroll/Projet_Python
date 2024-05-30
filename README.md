# Génération de trajectoires 

Voici quelques modules Python permettant de tester votre interface graphique sans ROS ni Turtlebot.

## Génération de trajectoire

La trajectoire est générée en format JSON à l'aide du script ``trajectory/make_trajectory.py``.

Les données sont au même format que les message ``Odometry`` fournis par l'interface ROS du Turtlebot, 
mais elles ne contiennent que le temps, la position et la vitesse linéaire dans le plan (les autres données sont fixées à 0).

La fréquence d'échantillonage est constante et dépend uniquement du nombre de points intermédiaire 
entre 2 points de la trajectoire.

Si vous désirez changer la trajectoire:
- modifiez sa définition à la fin du fichier ``trajectory/make_trajectory.py``
- installez ``numpy``: ``pip install numpy``
- exécutez le fichier: ``python3 ./trajectory/make_trajectory.py``.

La nouvelle trajectoire sera écrite dans le fichier ``trajectory/trajectory.json``.

## Utilisation dans votre programme

Le script ``trajectory/pose_subscriber.py`` fournit la même interface que ROS, à savoir une classe ``Subscriber``.

Pour l'utiliser dans votre programme, définissez une fonction qui sera appelée à chaque nouveau message lu:

```python
from trajectory.pose_subscriber import Subscriber, Odometry

def ma_fonction(message: Odometry):
    print(message.pose)

subcriber = Subscriber("/odom", Odometry, callback=ma_fonction)
```

Vous pouvez essayer d'éxecuter le script avec ``python3 ./trajectory/pose_subscriber.py``. 
