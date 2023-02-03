from detoxa_services.models.features import Feature
from django.contrib import admin
from  detoxa_services.models.appointments_models import  Appointment
from detoxa_services.models.child_tracker import ChildTracker
from detoxa_services.models.doctors_specialization import Specialization
from detoxa_services.models.eyesight_tracker import EyeSightTracker
from detoxa_services.models.favourites import Favourites
from detoxa_services.models.hand_eye_tracker import HandEyeTracker
from detoxa_services.models.orders import Cart, Order
from  detoxa_services.models.promocode_models import  Promocode
from detoxa_services.models.therapist import Therapist, TherapistCategory
from detoxa_services.models.therapy_session import TherapySession
from  detoxa_services.models.users import  Address, Users, UserActiveTokens
from detoxa_services.models.user_child_relation import  UserChildRelation
from detoxa_services.models.doctors_models import  Doctor, Speciality
from detoxa_services.models.reports_models import  UserGrowthReport, UserLearnabilityReport, UserMotorSkillsReport,UserHandEyeCoordinationReport,UserEyeSightReport,UserMedicalReport,UserAnalyticalReport
from detoxa_services.models.transactions_models import  Invoice, OrderTransaction, Transactions
from detoxa_services.models.testimonials import  Testimonials, Services
from detoxa_services.models.kits_models import  KitCategory, Kit, KitImages
from detoxa_services.models.learnability_tracker import LearnabilityTracker,LearnalityTrackerSectionAnswers
from detoxa_services.models.blogs import BlogCategory, Blog
from detoxa_services.models.organizations_models import  Organizations,OrganizationUser
from detoxa_services.models.doctors import BankDetails, Doctors
from detoxa_services.models.food_nutrition_models import  FoodNutrition
from detoxa_services.models.hospitals_models import  Hospital, HospitalUser
from detoxa_services.models.motor_skills import MotorSkillTracker, MotorSkillTrackerSectionAnswers
from detoxa_services.models.notification_models import Notifications
from detoxa_services.models.vaccination import VaccinationAppointment, VaccinationData,MyVaccinationDetails
from detoxa_services.models.meals_models import RecommendedMeals
from detoxa_services.models.analytical_tracker import AnalyticalTracker
from detoxa_services.models.country import CountryStates, Animals, Country, Vehicle, Profession, SolorSystem

admin.site.register(Appointment)
admin.site.register(Promocode)
admin.site.register(Users)
admin.site.register(UserActiveTokens)
admin.site.register(UserChildRelation)
admin.site.register(UserLearnabilityReport)
admin.site.register(UserGrowthReport)
admin.site.register(Speciality)
admin.site.register(Transactions)
admin.site.register(Testimonials)
admin.site.register(Services)
admin.site.register(Kit)
admin.site.register(KitCategory)
admin.site.register(KitImages)
admin.site.register(LearnabilityTracker)
admin.site.register(ChildTracker)
admin.site.register(BlogCategory)
admin.site.register(Blog)
admin.site.register(Organizations)
admin.site.register(OrganizationUser)
admin.site.register(Doctors)
admin.site.register(EyeSightTracker)
admin.site.register(HandEyeTracker)
admin.site.register(FoodNutrition)
admin.site.register(Hospital)
admin.site.register(HospitalUser)
admin.site.register(MotorSkillTracker)
admin.site.register(MotorSkillTrackerSectionAnswers)
admin.site.register(LearnalityTrackerSectionAnswers)
admin.site.register(UserMotorSkillsReport)
admin.site.register(UserHandEyeCoordinationReport)
admin.site.register(UserEyeSightReport)
admin.site.register(UserMedicalReport)
admin.site.register(Notifications)
admin.site.register(VaccinationData)
admin.site.register(MyVaccinationDetails)
admin.site.register(VaccinationAppointment)
admin.site.register(RecommendedMeals)
admin.site.register(UserAnalyticalReport)
admin.site.register(AnalyticalTracker)
admin.site.register(Specialization)
admin.site.register(Favourites)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderTransaction)
admin.site.register(Invoice)
admin.site.register(Therapist)
admin.site.register(TherapistCategory)
admin.site.register(TherapySession)
admin.site.register(BankDetails)
admin.site.register(Feature)
admin.site.register(Cart)
admin.site.register(CountryStates)
admin.site.register(Animals)
admin.site.register(Country)
admin.site.register(Vehicle)
admin.site.register(SolorSystem)
admin.site.register(Profession)





