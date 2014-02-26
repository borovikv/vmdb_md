"""
Created on Jul 9, 2013

@author: drifter
"""
from django.contrib import admin
from dbe.models import BranchTitle, Branch, BusinessEntityTitle, \
    BusinessEntityType, Brand, ContactPerson, Enterprise, Phone, Contact, \
    EnterpriseTitle, Gproduce, Advertisement, AdvertisementText, Url, Email, \
    PersonTitle, Person, PositionTitle, Position, GoodTitle, Good, \
    AdministrativeUnitTitle, TopAdministrativeUnit, RegionTitle, Region, \
    TownTitle, Town, SectorTitle, Sector, StreetTitle, Street, Language


class BranchTitleInline(admin.TabularInline):
    model = BranchTitle
    exclude = ('last_change',)


class BranchAdmin(admin.ModelAdmin):
    inlines = [BranchTitleInline, ]
    exclude = ('last_change',)


class BusinessEntityTitleInline(admin.TabularInline):
    model = BusinessEntityTitle
    exclude = ('last_change',)


class BusinessEntityAdmin(admin.ModelAdmin):
    inlines = [BusinessEntityTitleInline, ]
    exclude = ('last_change',)


class ContactPersonAdmin(admin.TabularInline):
    model = ContactPerson
    filter_horizontal = ('phones',)
    extra = 1
    exclude = ('last_change',)


class EnterpriseNameInline(admin.TabularInline):
    model = EnterpriseTitle
    exclude = ('last_change',)


class ContactInline(admin.StackedInline):
    model = Contact
    filter_horizontal = ('phones', 'urls', 'emails')
    extra = 1
    exclude = ('last_change',)


class GproduceInline(admin.TabularInline):
    model = Gproduce
    exclude = ('last_change',)


class AdvertismentInline(admin.TabularInline):
    model = Advertisement
    exclude = ('last_change',)


class AdvertismentTextInline(admin.TabularInline):
    model = AdvertisementText
    exclude = ('last_change',)

class AdvertismentAdmin(admin.ModelAdmin):
    inlines = [AdvertismentTextInline, ]
    exclude = ('last_change',)


class EnterpriseAdmin(admin.ModelAdmin):
    inlines = [ContactPersonAdmin, EnterpriseNameInline, ContactInline,
               GproduceInline, AdvertismentInline]
    exclude = ('last_change',)
    filter_horizontal = ('brands', )


class StreetTitleInline(admin.TabularInline):
    model = StreetTitle
    exclude = ('last_change',)


class StreetAdmin(admin.ModelAdmin):
    inlines = [StreetTitleInline]
    exclude = ('last_change',)


class SectorTitleInline(admin.TabularInline):
    model = SectorTitle
    exclude = ('last_change',)


class SectorAdmin(admin.ModelAdmin):
    inlines = [SectorTitleInline]
    exclude = ('last_change',)


class TownTitleInline(admin.TabularInline):
    model = TownTitle
    exclude = ('last_change',)


class TownAdmin(admin.ModelAdmin):
    inlines = [TownTitleInline]
    exclude = ('last_change',)


class RegionTitleInline(admin.TabularInline):
    model = RegionTitle
    exclude = ('last_change',)


class RegionAdmin(admin.ModelAdmin):
    inlines = [RegionTitleInline]
    exclude = ('last_change',)


class AdministrativeUnitTitleInline(admin.TabularInline):
    model = AdministrativeUnitTitle
    exclude = ('last_change',)


class TopAdministrativeUnitAdmin(admin.ModelAdmin):
    inlines = [AdministrativeUnitTitleInline]
    exclude = ('last_change',)


class GoodTitleInline(admin.TabularInline):
    model = GoodTitle
    exclude = ('last_change',)


class GoodAdmin(admin.ModelAdmin):
    inlines = [GoodTitleInline]
    exclude = ('last_change',)


class PositionTitleInline(admin.TabularInline):
    model = PositionTitle
    exclude = ('last_change',)


class PositionAdmin(admin.ModelAdmin):
    inlines = [PositionTitleInline]
    exclude = ('last_change',)


class PersonNameInline(admin.TabularInline):
    model = PersonTitle
    exclude = ('last_change',)


class PersonAdmin(admin.ModelAdmin):
    inlines = [PersonNameInline]
    exclude = ('last_change',)


admin.site.register(Language)
admin.site.register(Branch, BranchAdmin)
admin.site.register(BusinessEntityType, BusinessEntityAdmin)
admin.site.register(Brand)
admin.site.register(Phone)
admin.site.register(Url)
admin.site.register(Email)
admin.site.register(Enterprise, EnterpriseAdmin)
admin.site.register(Advertisement, AdvertismentAdmin)
admin.site.register(Street, StreetAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(Town, TownAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(TopAdministrativeUnit, TopAdministrativeUnitAdmin)
admin.site.register(Good, GoodAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Person, PersonAdmin)
