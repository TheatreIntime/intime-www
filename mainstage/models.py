from django.db import models

# Create your models here.

'''
Important Vocabulary

Season: A collection of plays throughout a year.
Play: A production with writer, director, and cast that has numerous shows.
Show: One date on which a play is performed.
Cast: A group of students in a play and their roles.
Student: Specifically a Princeton Student.
'''

class Season(models.Model):
	end_year = models.PositiveSmallIntegerField(unique=True)
	is_current = models.BooleanField()
	current_play = models.ForeignKey(Play)
	audition_play = models.ForeignKey(Play)

	def __unicode__(self):
		return u"%s-%s Season" % (end_year-1, end_year)

class Play(models.Model):
	season = models.ForeignKey(Season);
	title = models.CharField(max_length=50)
	blurb = models.TextField()
	writer = models.CharField(max_length=70)
	director = models.ForeignKey(Student)

	# By Default, use Theatre Intime's Logo
	poster = models.URLField(default="https://pbs.twimg.com/profile_images/3628492222/de57d0de343e4818a64ea41bd3b84bf9.jpeg")

	# Used for Play Groups like OAF and 24-Hour
	# 0 = Nothing to do with play group
	# 1 = Root of play group
	# 2 = In a play group, see foreign key for group
	playgroup = models.PositiveSmallIntegerField(default=0)
	playgroup_root = models.ForeignKey(Play, blank=True)

	def in_a_playgroup(self):
		return (self.playgroup == 2)

	def __unicode__(self):
		return self.title

class Show(models.Model):
	play = models.ForeignKey(Play)
	showtime = models.DateTimeField()

	# Not used now, eventually used for ticket sales
	ticket_id = models.SlugField()

class Cast(models.Model):
	actor = models.ForeignKey(Student)
	role = models.CharField(max_length = 100)
	play = models.ForeignKey(Play)

	def __unicode__(self):
		return u"%s as %s in %s" % (actor.name, role, play.title)

class Student(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	netid = models.CharField(max_length=50)
	class_year = models.PositiveSmallIntegerField()
	bio = models.TextField()
	pic = models.URLField()

	def _get_name(self):
		return u"%s %s" % (self.first_name, self.last_name)
	name = property(_get_name)

	def __unicode__(self):
		return name