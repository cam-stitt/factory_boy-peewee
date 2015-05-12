from __future__ import unicode_literals
from __future__ import absolute_import
import peewee

from factory import base


class PeeweeOptions(base.FactoryOptions):
    def _build_default_options(self):
        return super(PeeweeOptions, self)._build_default_options() + [
            base.OptionDefault('database', None, inherit=True),
        ]


class PeeweeModelFactory(base.Factory):
    """Factory for peewee models. """

    _options_class = PeeweeOptions

    class Meta:
        abstract = True

    @classmethod
    def _setup_next_sequence(cls, *args, **kwargs):
        """Compute the next available PK, based on the 'pk' database field."""
        db = cls._meta.database
        model = cls._meta.model
        pk = getattr(model, model._meta.primary_key.name)
        max_pk = model.select(
            model, peewee.fn.Max(pk).alias('maxpk')
        ).limit(1).execute()
        max_pk = [mp.maxpk for mp in max_pk][0]
        if isinstance(max_pk, int):
            return max_pk + 1 if max_pk else 1
        else:
            return 1

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        db = cls._meta.database
        obj = target_class.create(**kwargs)
        return obj
