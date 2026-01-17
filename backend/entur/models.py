from datetime import datetime
from enum import Enum
from typing import Any
from pydantic import BaseModel, Field, RootModel, ConfigDict


# Enums based on OpenAPI schema
class TransportMode(str, Enum):
    AIR = "AIR"
    BUS = "BUS"
    COACH = "COACH"
    FERRY = "FERRY"
    METRO = "METRO"
    RAIL = "RAIL"
    TROLLEY_BUS = "TROLLEY_BUS"
    TRAM = "TRAM"
    WATER = "WATER"
    CABLEWAY = "CABLEWAY"
    FUNICULAR = "FUNICULAR"
    LIFT = "LIFT"
    SNOW_AND_ICE = "SNOW_AND_ICE"
    OTHER = "OTHER"


class StopPlaceType(str, Enum):
    ONSTREET_BUS = "ONSTREET_BUS"
    ONSTREET_TRAM = "ONSTREET_TRAM"
    AIRPORT = "AIRPORT"
    RAIL_STATION = "RAIL_STATION"
    METRO_STATION = "METRO_STATION"
    BUS_STATION = "BUS_STATION"
    COACH_STATION = "COACH_STATION"
    TRAM_STATION = "TRAM_STATION"
    HARBOUR_PORT = "HARBOUR_PORT"
    FERRY_PORT = "FERRY_PORT"
    FERRY_STOP = "FERRY_STOP"
    LIFT_STATION = "LIFT_STATION"
    VEHICLE_RAIL_INTERCHANGE = "VEHICLE_RAIL_INTERCHANGE"
    OTHER = "OTHER"


class AccessibilityValue(str, Enum):
    TRUE = "TRUE"
    FALSE = "FALSE"
    UNKNOWN = "UNKNOWN"
    PARTIAL = "PARTIAL"


class ModificationStatus(str, Enum):
    NEW = "NEW"
    REVISE = "REVISE"
    DELETE = "DELETE"
    UNCHANGED = "UNCHANGED"
    DELTA = "DELTA"


class PublicationStatus(str, Enum):
    PUBLIC = "PUBLIC"
    RESTRICTED = "RESTRICTED"
    PRIVATE = "PRIVATE"
    CONFIDENTIAL = "CONFIDENTIAL"
    AUTHORISED = "AUTHORISED"
    TEST = "TEST"


class ActivationStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    OTHER = "OTHER"


class Weighting(str, Enum):
    NO_INTERCHANGE = "NO_INTERCHANGE"
    INTERCHANGE_ALLOWED = "INTERCHANGE_ALLOWED"
    RECOMMENDED_INTERCHANGE = "RECOMMENDED_INTERCHANGE"
    PREFERRED_INTERCHANGE = "PREFERRED_INTERCHANGE"


class ModificationSet(str, Enum):
    ALL = "ALL"
    CHANGES_ONLY = "CHANGES_ONLY"


class NameType(str, Enum):
    ALIAS = "ALIAS"
    TRANSLATION = "TRANSLATION"
    COPY = "COPY"
    LABEL = "LABEL"
    OTHER = "OTHER"


# Core data models
class Location(BaseModel):
    latitude: float
    longitude: float
    altitude: float | None = None
    srsName: str | None = None


class Centroid(BaseModel):
    location: Location
    id: str | None = None


class LocalizedString(BaseModel):
    lang: str
    value: str | None = None
    textIdType: str | None = None


class KeyValue(BaseModel):
    key: str
    value: str | None = None
    typeOfKey: str | None = None


class KeyList(BaseModel):
    keyValue: list[KeyValue] = Field(default_factory=list)


class PrivateCode(BaseModel):
    value: str | None = None
    type: str | None = None


class AccessibilityLimitation(BaseModel):
    id: str | None = None
    wheelchairAccess: AccessibilityValue | None = None
    stepFreeAccess: AccessibilityValue | None = None
    escalatorFreeAccess: AccessibilityValue | None = None
    liftFreeAccess: AccessibilityValue | None = None
    audibleSignalsAvailable: AccessibilityValue | None = None
    visualSignsAvailable: AccessibilityValue | None = None
    version: str | None = None
    modification: ModificationStatus | None = None
    publication: PublicationStatus | None = None
    status_BasicModificationDetailsGroup: ActivationStatus | None = Field(
        None, alias="status_BasicModificationDetailsGroup"
    )


class Limitations(BaseModel):
    accessibilityLimitation: AccessibilityLimitation | None = None


class AccessibilityAssessment(BaseModel):
    id: str | None = None
    limitations: Limitations | None = None
    mobilityImpairedAccess: AccessibilityValue | None = None
    version: str | None = None
    modification: ModificationStatus | None = None
    publication: PublicationStatus | None = None
    status_BasicModificationDetailsGroup: ActivationStatus | None = Field(
        None, alias="status_BasicModificationDetailsGroup"
    )


class Quay(BaseModel):
    id: str
    publicCode: str | None = None
    privateCode: PrivateCode | None = None
    description: LocalizedString | None = None
    centroid: Centroid | None = None
    accessibilityAssessment: AccessibilityAssessment | None = None
    keyList: KeyList | None = None
    changed: datetime | None = None
    created: datetime | None = None
    version: str | None = None
    modification: ModificationStatus | None = None
    publication: PublicationStatus | None = None
    status_BasicModificationDetailsGroup: ActivationStatus | None = Field(
        None, alias="status_BasicModificationDetailsGroup"
    )

    model_config = ConfigDict(populate_by_name=True)


class Quays(BaseModel):
    modificationSet: ModificationSet | None = None
    quayRefOrQuay: list[Quay] = Field(default_factory=list)


class TariffZoneRef(BaseModel):
    ref: str
    version: str | None = None
    created: datetime | None = None
    changed: datetime | None = None


class TariffZones(BaseModel):
    modificationSet: ModificationSet | None = None
    tariffZoneRef: list[TariffZoneRef] = Field(default_factory=list)


class SiteRef(BaseModel):
    ref: str
    version: str | None = None
    created: datetime | None = None
    changed: datetime | None = None
    modification: ModificationStatus | None = None


class AlternativeName(BaseModel):
    id: str | None = None
    name: LocalizedString
    nameType: NameType | None = None
    lang: str | None = None
    shortName: LocalizedString | None = None
    version: str | None = None
    modification: ModificationStatus | None = None
    publication: PublicationStatus | None = None
    status_BasicModificationDetailsGroup: ActivationStatus | None = Field(
        None, alias="status_BasicModificationDetailsGroup"
    )

    model_config = ConfigDict(populate_by_name=True)


class AlternativeNames(BaseModel):
    alternativeName: list[AlternativeName] = Field(default_factory=list)


class TopographicPlaceView(BaseModel):
    id: str | None = None
    name: LocalizedString | None = None
    shortName: LocalizedString | None = None
    qualifierName: LocalizedString | None = None
    topographicPlaceRef: SiteRef | None = None


class PlaceEquipment(BaseModel):
    id: str | None = None
    installedEquipmentRefOrInstalledEquipment: list[Any] = Field(default_factory=list)
    modificationSet: ModificationSet | None = None


class StopPlace(BaseModel):
    """
    NeTEx StopPlace model for Entur API.
    Represents a physical location where passengers can board or alight from public transport.
    """

    # Required fields
    id: str
    name: LocalizedString

    # Geographic location
    centroid: Centroid | None = None

    # Classification
    transportMode: TransportMode | None = None
    stopPlaceType: StopPlaceType | None = None
    weighting: Weighting | None = None

    # Related structures
    quays: Quays | None = None
    tariffZones: TariffZones | None = None

    # References
    topographicPlaceRef: SiteRef | None = None
    topographicPlaceView: TopographicPlaceView | None = None
    parentSiteRef: SiteRef | None = None
    parentZoneRef: SiteRef | None = None

    # Accessibility
    accessibilityAssessment: AccessibilityAssessment | None = None
    allAreasWheelchairAccessible: bool | None = None

    # Names and identifiers
    alternativeNames: AlternativeNames | None = None
    shortName: LocalizedString | None = None
    description: LocalizedString | None = None
    keyList: KeyList | None = None
    privateCode: PrivateCode | dict[str, Any] | None = None
    publicCode: str | None = None

    # Equipment and facilities
    placeEquipments: PlaceEquipment | None = None

    # Other transport modes available
    otherTransportModes: list[TransportMode] | None = None

    # Temporal data
    created: datetime | None = None
    changed: datetime | None = None

    # Version control
    version: str | None = None
    modification: ModificationStatus | None = None
    publication: PublicationStatus | None = None
    status_BasicModificationDetailsGroup: ActivationStatus | None = Field(
        None, alias="status_BasicModificationDetailsGroup"
    )

    model_config = ConfigDict(populate_by_name=True)


class StopPlacesResponse(RootModel[list[StopPlace]]):
    """
    Response model for the /stop-places endpoint.
    Returns a list of StopPlace objects from the Entur API.
    """

    root: list[StopPlace]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]

    def __len__(self):
        return len(self.root)


class Codespace(Enum):
    """Norwegian public transport operator codespaces"""
    AKT = "akt"  # Agder kollektivtrafikk
    ATB = "atb"  # AtB (Trøndelag)
    ASH = "ash"  # Arctic Sea Hotel & Apartments
    AVI = "avi"  # Avinor
    BNR = "bnr"  # Bane NOR
    BEF = "bef"  # Beffen
    BOR = "bor"  # Boreal
    BSR = "bsr"  # Bussring
    BRA = "bra"  # Brakar (Buskerud)
    NYC = "nyc"  # Bygdøyfergen
    COL = "col"  # Color Line
    TEL = "tel"  # Farte (Telemark)
    FJT = "fjt"  # Fjord Tours
    FLI = "fli"  # Flixbus
    FLT = "flt"  # Flytoget
    FTR = "ftr"  # Flåm Travel
    FLB = "flb"  # Flåmsbana
    OSC = "osc"  # Forsvarsbygg (Oscarsborgfergen)
    MOR = "mor"  # Fram (Møre og Romsdal)
    GFS = "gfs"  # Geiranger Fjordservice
    GLO = "glo"  # GlobeOrbit100
    GOA = "goa"  # Go Ahead
    GOF = "gof"  # Go Fjords
    HAF = "haf"  # Hafjell Alpinsenter
    HAV = "hav"  # Havila
    HUR = "hur"  # Hurtigruten
    HOG = "hog"  # Høgsfjordferja
    INN = "inn"  # Innlandet
    KOL = "kol"  # Kolumbus (Rogaland)
    SOF = "sof"  # Kringom (Sogn og Fjordane)
    OIS = "ois"  # MF Øisang
    NWY = "nwy"  # NOR-WAY Bussekspress
    NOR = "nor"  # Nordland fylkeskommune
    NBU = "nbu"  # Connect Bus Flybuss
    NIA = "nia"  # Norsk industrianlegg
    VIP = "vip"  # Oslo VIP Transporttjenester
    RUT = "rut"  # Ruter (Oslo & Akershus)
    SJV = "sjv"  # SJ
    SJN = "sjn"  # SJ NORD
    SKY = "sky"  # Skyss (Hordaland)
    FIN = "fin"  # Snelandia (Finnmark)
    STB = "stb"  # Stadbussen
    TID = "tid"  # Tide
    TRO = "tro"  # Troms fylkestrafikk
    TTS = "tts"  # Torghatten
    ULR = "ulr"  # Ulriken
    UNI = "uni"  # Unibuss
    VOT = "vot"  # Vestfold og Telemark
    VIL = "vil"  # Visit Lillehammer
    VKT = "vkt"  # VKT (Vestfold)
    VOG = "vog"  # Voss Gondol
    NSB = "nsb"  # Vy (formerly NSB)
    GJB = "gjb"  # Vy (formerly NSB) Gjøvikbanen
    VYG = "vyg"  # Vy-group
    VYB = "vyb"  # Vy Buss AB
    VYX = "vyx"  # Vy Buss AS
    OST = "ost"  # Østfold kollektivtrafikk
    ATU = "atu"  # Ålesund Turvogn Service
