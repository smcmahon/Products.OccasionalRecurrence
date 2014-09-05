from zope.component import adapts
from zope.interface import implements

from Products.ATContentTypes.interface import IATEvent
from Products.Archetypes import public as atapi

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaModifier

from Products.OccasionalRecurrence.interfaces import IProductsOccasionalRecurrenceLayer

from Products.OccasionalRecurrence import OccasionalRecurrenceMessageFactory as _


class _ExtensionStringField(ExtensionField, atapi.StringField):
    """ Retrofitted string field """


class EventExtender(object):
    """ Include recurrence option on events.
    """

    # This extender will apply to all Archetypes based content
    adapts(IATEvent)

    # We use both orderable and browser layer aware sensitive properties
    implements(IOrderableSchemaExtender, IBrowserLayerAwareExtender)

    # Don't do schema extending unless our add-on product is installed on Plone site
    layer = IProductsOccasionalRecurrenceLayer

    fields = [
        _ExtensionStringField(
            'recurs',
            vocabulary=atapi.DisplayList((
                ('daily', _(u"Daily")),
                ('weekly', _(u"Weekly")),
                ('biweekly', _(u"Biweekly")),
                ('monthly', _(u"Monthy")),
            )),
            widget=atapi.SelectionWidget(
                label=_(u"Occurs"),
                description=_(u"Frequency of Occurence"),
            ),
            required=True,
            default='daily',
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        """ Manipulate the order in which fields appear.

        @param schematas: Dictonary of schemata name -> field lists

        @return: Dictionary of reordered field lists per schemata.
        """
        schematas["default"] =  ['id', 'title', 'description', 'location', 'startDate', 'recurs', 'endDate', 'text', 'attendees', 'eventUrl', 'contactName', 'contactEmail', 'contactPhone']

        return schematas

    def getFields(self):
        """
        @return: List of new fields we contribute to content.
        """
        return self.fields


class EventFiddler(object):
    """ Include recurrence option on events.
    """

    adapts(IATEvent)
    implements(ISchemaModifier)

    # Don't do schema extending unless our add-on product is installed on Plone site
    layer = IProductsOccasionalRecurrenceLayer

    def __init__(self, context):
        self.context = context

    def fiddle(self, schema):
        """ adapt end date """

        new_field = schema['endDate'].copy()

        new_field.widget.label = _(u"Until")
        new_field.widget.description = ''

        schema['endDate'] = new_field
