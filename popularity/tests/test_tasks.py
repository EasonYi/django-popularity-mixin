# -*- coding: utf-8 -*-

from django.conf import settings
from django.test import TestCase
from django.core.cache import cache
from django.contrib.sites.models import Site

from popularity.tasks import HitCountJob


class HitCountJobTest(TestCase):

    def setUp(self):
        self.object = Site.objects.get_or_create(pk=settings.SITE_ID)[0]
        self.job = HitCountJob()

    def tearDown(self):
        cache.clear()

    def test_caching(self):
        opts, object_id = self.object._meta, self.object.pk

        with self.assertNumQueries(2):
            hits = self.job.get(opts.app_label, opts.module_name, object_id)

        self.assertEqual(hits['total'], 0)

        with self.assertNumQueries(0):
            hits = self.job.get(opts.app_label, opts.module_name, object_id)

        self.assertEqual(hits['total'], 0)  # returns cached result
