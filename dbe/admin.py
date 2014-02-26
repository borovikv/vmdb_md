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


class BranchAdmin(admin.ModelAdmin):
    inlines = [BranchTitleInline, ]


class BusinessEntityTitleInline(admin.TabularInline):
    model = BusinessEntityTitle


class BusinessEntityAdmin(admin.ModelAdmin):
    inlines = [BusinessEntityTitleInline, ]


class ContactPersonAdmin(admin.TabularInline):
    model = ContactPerson
    filter_horizontal = ('phones',)
    extra = 1


class EnterpriseNameInline(admin.TabularInline):
    model = EnterpriseTitle


class ContactInline(admin.StackedInline):
    model = Contact
    filter_horizontal = ('phones', 'urls', 'emails')
    extra = 1


class GproduceInline(admin.TabularInline):
    model = Gproduce


class AdvertismentInline(admin.TabularInline):
    model = Advertisement


class AdvertismentTextInline(admin.TabularInline):
    model = AdvertisementText


class AdvertismentAdmin(admin.ModelAdmin):
    inlines = [AdvertismentTextInline, ]


class EnterpriseAdmin(admin.ModelAdmin):
    inlines = [ContactPersonAdmin, EnterpriseNameInline, ContactInline,
               GproduceInline, AdvertismentInline]
    exclude = ('last_change',)
    filter_horizontal = ('brands', )


class StreetTitleInline(admin.TabularInline):
    model = StreetTitle


class StreetAdmin(admin.ModelAdmin):
    inlines = [StreetTitleInline]


class SectorTitleInline(admin.TabularInline):
    model = SectorTitle


class SectorAdmin(admin.ModelAdmin):
    inlines = [SectorTitleInline]


class TownTitleInline(admin.TabularInline):
    model = TownTitle


class TownAdmin(admin.ModelAdmin):
    inlines = [TownTitleInline]


class RegionTitleInline(admin.TabularInline):
    model = RegionTitle


class RegionAdmin(admin.ModelAdmin):
    inlines = [RegionTitleInline]


class AdministrativeUnitTitleInline(admin.TabularInline):
    model = AdministrativeUnitTitle


class TopAdministrativeUnitAdmin(admin.ModelAdmin):
    inlines = [AdministrativeUnitTitleInline]


class GoodTitleInline(admin.TabularInline):
    model = GoodTitle


class GoodAdmin(admin.ModelAdmin):
    inlines = [GoodTitleInline]


class PositionTitleInline(admin.TabularInline):
    model = PositionTitle


class PositionAdmin(admin.ModelAdmin):
    inlines = [PositionTitleInline]


class PersonNameInline(admin.TabularInline):
    model = PersonTitle


class PersonAdmin(admin.ModelAdmin):
    inlines = [PersonNameInline]


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
