from rest_framework.generics import ListAPIView, UpdateAPIView,CreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from detoxa_services.serializers.feature_serializer import FeatureSerializer,UpdateFeatureSerializer
from detoxa_services.models.features import Feature
from detoxa_services.utils.user_authentication import UserAuthentication

class FeatureListView(ListAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        # logged_in_user = UserAuthentication.authenticate(self, request)[0]
        # if logged_in_user.is_admin:
        queryset = Feature.objects.all()
        # serializer = FeatureSerializer(queryset, many=False)
        return Response({"message": "List of all features fetched successfully",'data':queryset.values()}, status=HTTP_200_OK)
        # else:
        #     return Response({"message": "You are not authorized to perform this action"}, status=HTTP_400_BAD_REQUEST)

class UpdateFeatureView(UpdateAPIView):
    queryset = Feature.objects.all()
    serializer_class = UpdateFeatureSerializer

    def put(self, request, *args, **kwargs):
        logged_in_user = UserAuthentication.authenticate(self, request)[0]
        if logged_in_user.is_admin:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                try:
                    feature_obj = Feature.objects.filter(id=1)[0]
                    for i in serializer.validated_data['enable_features']:
                        try:
                            if i == 'Home_Choose_Your_Subscription':
                                feature_obj.Home_Choose_Your_Subscription = True
                                feature_obj.save()
                            if i == 'Home_Child_Tracker':
                                feature_obj.Home_Child_Tracker = True
                                feature_obj.save()
                            if i == 'Home_Latest_Video':
                                feature_obj.Home_Latest_Video = True
                                feature_obj.save()
                            if i == 'Home_Specialities':
                                feature_obj.Home_Specialities = True
                                feature_obj.save()
                            if i == 'Home_Why_Detoxa':
                                feature_obj.Home_Why_Detoxa = True
                                feature_obj.save()
                            if i == 'Home_Feedback':
                                feature_obj.Home_Feedback = True
                                feature_obj.save()
                            if i == 'Navigation_Bar_Child_Tracker':
                                feature_obj.Navigation_Bar_Child_Tracker = True
                                feature_obj.save()
                            if i == 'Navigation_Bar_Consultation':
                                feature_obj.Navigation_Bar_Consultation = True
                                feature_obj.save()
                            if i == 'Navigation_Bar_Therapy':
                                feature_obj.Navigation_Bar_Therapy = True
                                feature_obj.save()
                            if i == 'Navigation_Bar_Subscription':
                                feature_obj.Navigation_Bar_Subscription = True
                                feature_obj.save()
                            if i == 'Navigation_Bar_Covid-19':
                                feature_obj.Navigation_Bar_Covid_19 = True
                                feature_obj.save()
                            if i == 'Navigation_Bar_Blogs':
                                feature_obj.Navigation_Bar_Blogs = True
                                feature_obj.save()
                            if i == 'Navigation_Bar_Child_Kits':
                                feature_obj.Navigation_Bar_Child_Kits = True
                                feature_obj.save()
                            if i == 'Navigation_Bar_Contact':
                                feature_obj.Navigation_Bar_Contact = True
                                feature_obj.save()
                            if i == 'Child_Tracker_Growth':
                                feature_obj.Child_Tracker_Growth = True
                                feature_obj.save()
                            if i == 'Child_Tracker_Eyesight':
                                feature_obj.Child_Tracker_Eyesight = True
                                feature_obj.save()
                            if i == 'Child_Tracker_Vaccination':
                                feature_obj.Child_Tracker_Vaccination = True
                                feature_obj.save()
                            if i == 'Child_Tracker_Food_and_Nutrition':
                                feature_obj.Child_Tracker_Food_and_Nutrition = True
                                feature_obj.save()
                            if i == 'Child_Tracker_Hand_and_Eye_Coordination':
                                feature_obj.Child_Tracker_Hand_and_Eye_Coordination = True
                                feature_obj.save()
                            if i == 'Child_Tracker_Learnability':
                                feature_obj.Child_Tracker_Learnability = True
                                feature_obj.save()
                            if i == 'Child_Tracker_Analytical':
                                feature_obj.Child_Tracker_Analytical = True
                                feature_obj.save()
                            if i == 'Child_Tracker_Motor_Skill':
                                feature_obj.Child_Tracker_Motor_Skill = True
                                feature_obj.save()
                            if i == 'Child_Tracker_Skin':
                                feature_obj.Child_Tracker_Skin = True
                                feature_obj.save()
                            if i == 'Child_Tracker_Hair':
                                feature_obj.Child_Tracker_Hair = True
                                feature_obj.save()
                            if i == 'Growth_Tracker_Child_Details':
                                feature_obj.Growth_Tracker_Child_Details = True
                                feature_obj.save()
                            if i == 'Growth_Tracker_View_Reports':
                                feature_obj.Growth_Tracker_View_Reports = True
                                feature_obj.save()
                            if i == 'Growth_Tracker_Testimonials':
                                feature_obj.Growth_Tracker_Testimonials = True
                                feature_obj.save()
                            if i == 'Eyesight_Tracker_Child_Details':
                                feature_obj.Eyesight_Tracker_Child_Details = True
                                feature_obj.save()
                            if i == 'Eyesight_Tracker_View_Reports':
                                feature_obj.Eyesight_Tracker_View_Reports = True
                                feature_obj.save()
                            if i == 'Eyesight_Tracker_Testimonials':
                                feature_obj.Eyesight_Tracker_Testimonials = True
                                feature_obj.save()
                            if i == 'Vaccination_Tracker_Child_Details':
                                feature_obj.Vaccination_Tracker_Child_Details = True
                                feature_obj.save()
                            if i == 'Vaccination_Tracker_View_Reports':
                                feature_obj.Vaccination_Tracker_View_Reports = True
                                feature_obj.save()
                            if i == 'Vaccination_Tracker_Testimonials':
                                feature_obj.Vaccination_Tracker_Testimonials = True
                                feature_obj.save()
                            if i == 'Food_Tracker_Child_Details':
                                feature_obj.Food_Tracker_Child_Details = True
                                feature_obj.save()
                            if i == 'Food_Tracker_Recommended_Meals':
                                feature_obj.Food_Tracker_Recommended_Meals = True
                                feature_obj.save()
                            if i == 'Food_Tracker_View_Reports':
                                feature_obj.Food_Tracker_View_Reports = True
                                feature_obj.save()
                            if i == 'Food_Tracker_Child_Testimonials':
                                feature_obj.Food_Tracker_Child_Testimonials = True
                                feature_obj.save()
                            if i == 'Hand_and_Eye_Tracker_Child_Details':
                                feature_obj.Hand_and_Eye_Tracker_Child_Details = True
                                feature_obj.save()
                            if i == 'Hand_and_Eye_Tracker_View_Reports':
                                feature_obj.Hand_and_Eye_Tracker_View_Reports = True
                                feature_obj.save()
                            if i == 'Hand_and_Eye_Tracker_Testimonials':
                                feature_obj.Hand_and_Eye_Tracker_Testimonials = True
                                feature_obj.save()
                            if i == 'Learnability_Tracker_Child_Details':
                                feature_obj.Learnability_Tracker_Child_Details = True
                                feature_obj.save()
                            if i == 'Learnability_Tracker_View_Reports':
                                feature_obj.Learnability_Tracker_View_Reports = True
                                feature_obj.save()
                            if i == 'Learnability_Tracker_Testimonials':
                                feature_obj.Learnability_Tracker_Testimonials = True
                                feature_obj.save()
                            if i == 'Analytical_Tracker_Child_Details':
                                feature_obj.Analytical_Tracker_Child_Details = True
                                feature_obj.save()
                            if i == 'Analytical_Tracker_View_Reports':
                                feature_obj.Analytical_Tracker_View_Reports = True
                                feature_obj.save()
                            if i == 'Analytical_Tracker_Testimonials':
                                feature_obj.Analytical_Tracker_Testimonials = True
                                feature_obj.save()
                            if i == 'Motor_Skill_Tracker_Child_Details':
                                feature_obj.Motor_Skill_Tracker_Child_Details = True
                                feature_obj.save()
                            if i == 'Motor_Skill_Tracker_View_Reports':
                                feature_obj.Motor_Skill_Tracker_View_Reports = True
                                feature_obj.save()
                            if i == 'Motor_Skill_Tracker_Testimonials':
                                feature_obj.Motor_Skill_Tracker_Testimonials = True
                                feature_obj.save()
                            if i == 'Skin_Tracker_Child_Details':
                                feature_obj.Skin_Tracker_Child_Details = True
                                feature_obj.save()
                            if i == 'Skin_Tracker_View_Reports':
                                feature_obj.Skin_Tracker_View_Reports = True
                                feature_obj.save()
                            if i == 'Skin_Tracker_Testimonials':
                                feature_obj.Skin_Tracker_Testimonials = True
                                feature_obj.save()
                            if i == 'Hair_Tracker_Child_Details':
                                feature_obj.Hair_Tracker_Child_Details = True
                                feature_obj.save()
                            if i == 'Hair_Tracker_View_Reports':
                                feature_obj.Hair_Tracker_View_Reports = True
                                feature_obj.save()
                            if i == 'Hair_Tracker_Testimonials':
                                feature_obj.Hair_Tracker_Testimonials = True
                                feature_obj.save()
                            if i == 'Consultation_Speciality':
                                feature_obj.Consultation_Speciality = True
                                feature_obj.save()
                            if i == 'Consultation_Search_Doctors':
                                feature_obj.Consultation_Search_Doctors = True
                                feature_obj.save()
                            if i == 'Consultation_Symptoms':
                                feature_obj.Consultation_Symptoms = True
                                feature_obj.save()
                            if i == 'Therapy_Speciality':
                                feature_obj.Therapy_Speciality = True
                                feature_obj.save()
                            if i == 'Therapy_Search_Doctors':
                                feature_obj.Therapy_Search_Doctors = True
                                feature_obj.save()
                            if i == 'Theraoy_Symptoms':
                                feature_obj.Theraoy_Symptoms = True
                                feature_obj.save()
                            if i == 'Subscription_Choose_Your_Subscription':
                                feature_obj.Subscription_Choose_Your_Subscription = True
                                feature_obj.save()
                            if i == 'Subscription_Membership':
                                feature_obj.Subscription_Membership = True
                                feature_obj.save()
                            if i == 'Subscription_Offers':
                                feature_obj.Subscription_Offers = True
                                feature_obj.save()
                            if i == 'Covid_Avoid_Covid':
                                feature_obj.Covid_Avoid_Covid = True
                                feature_obj.save()
                            if i == 'Covid_Symptoms':
                                feature_obj.Covid_Symptoms = True
                                feature_obj.save()
                            if i == 'Covid_Doctors':
                                feature_obj.Covid_Doctors = True
                                feature_obj.save()
                            if i == 'Covid_Screen_Time':
                                feature_obj.Covid_Screen_Time = True
                                feature_obj.save()
                            if i == 'Blogs_Trending_Blogs': 
                                feature_obj.Blogs_Trending_Blogs = True
                                feature_obj.save()
                            if i == 'Blogs_Categories':
                                feature_obj.Blogs_Categories = True
                                feature_obj.save()
                            if i == 'Blogs_Listing':
                                feature_obj.Blogs_Listing = True
                                feature_obj.save()
                            if i =='Kits_Categories':
                                feature_obj.Kits_Categories = True
                                feature_obj.save()
                            if i == 'Kits_Listing':
                                feature_obj.Kits_Categories = True
                                feature_obj.save()

                            # if i == 'home':
                            #     feature_obj.home = True
                            #     feature_obj.save()
                            # if i == 'growth_tracker':
                            #     feature_obj.growth_tracker = True
                            #     feature_obj.save()
                            # if i == 'eyesight_tracker':
                            #     feature_obj.eyesight_tracker = True
                            #     feature_obj.save()
                            # if i == 'vaccination_tracker':
                            #     feature_obj.vaccination_tracker = True
                            #     feature_obj.save()
                            # if i == 'food_nutrition_tracker':
                            #     feature_obj.food_nutrition_tracker = True
                            #     feature_obj.save()
                            # if i == 'hand_eye_tracker':
                            #     feature_obj.hand_eye_tracker = True
                            #     feature_obj.save()
                            # if i == 'learnability_tracker':
                            #     feature_obj.learnability_tracker = True
                            #     feature_obj.save()
                            # if i == 'analytical_tracker':
                            #     feature_obj.analytical_tracker = True
                            #     feature_obj.save()
                            # if i == 'motorskill_tracker':
                            #     feature_obj.motorskill_tracker = True
                            #     feature_obj.save()
                            # if i == 'skin_tracker':
                            #     feature_obj.skin_tracker = True
                            #     feature_obj.save()
                            # if i == 'hair_tracker':
                            #     feature_obj.hair_tracker = True
                            #     feature_obj.save()
                            # if i == 'consultation':
                            #     feature_obj.consultation = True
                            #     feature_obj.save()
                            # if i == 'therapy':
                            #     feature_obj.therapy = True
                            #     feature_obj.save()
                            # if i == 'subscription':
                            #     feature_obj.subscription = True
                            #     feature_obj.save()
                            # if i == 'covid_19':
                            #     feature_obj.covid_19 = True
                            #     feature_obj.save()
                            # if i == 'blogs':
                            #     feature_obj.blogs = True
                            #     feature_obj.save()
                            # if i == 'child_kits':
                            #     feature_obj.child_kits = True
                            #     feature_obj.save()
                            # if i == 'contact':
                            #     feature_obj.contact = True
                            #     feature_obj.save()
                        except Exception as e:
                            print(e)
                    for j in serializer.validated_data['disable_features']:
                        try:
                            if j == 'Home_Choose_Your_Subscription':
                                feature_obj.Home_Choose_Your_Subscription = False
                                feature_obj.save()
                            if j == 'Home_Child_Tracker':
                                feature_obj.Home_Child_Tracker = False
                                feature_obj.save()
                            if j == 'Home_Latest_Video':
                                feature_obj.Home_Latest_Video = False
                                feature_obj.save()
                            if j == 'Home_Specialities':
                                feature_obj.Home_Specialities = False
                                feature_obj.save()
                            if j == 'Home_Why_Detoxa':
                                feature_obj.Home_Why_Detoxa = False
                                feature_obj.save()
                            if j == 'Home_Feedback':
                                feature_obj.Home_Feedback = False
                                feature_obj.save()
                            if j == 'Navigation_Bar_Child_Tracker':
                                feature_obj.Navigation_Bar_Child_Tracker = False
                                feature_obj.save()
                            if j == 'Navigation_Bar_Consultation':
                                feature_obj.Navigation_Bar_Consultation = False
                                feature_obj.save()
                            if j == 'Navigation_Bar_Therapy':
                                feature_obj.Navigation_Bar_Therapy = False
                                feature_obj.save()
                            if j == 'Navigation_Bar_Subscription':
                                feature_obj.Navigation_Bar_Subscription = False
                                feature_obj.save()
                            if j == 'Navigation_Bar_Covid-19':
                                feature_obj.Navigation_Bar_Covid_19 = False
                                feature_obj.save()
                            if j == 'Navigation_Bar_Blogs':
                                feature_obj.Navigation_Bar_Blogs = False
                                feature_obj.save()
                            if j == 'Navigation_Bar_Child_Kits':
                                feature_obj.Navigation_Bar_Child_Kits = False
                                feature_obj.save()
                            if j == 'Navigation_Bar_Contact':
                                feature_obj.Navigation_Bar_Contact = False
                                feature_obj.save()
                            if j == 'Child_Tracker_Growth':
                                feature_obj.Child_Tracker_Growth = False
                                feature_obj.save()
                            if j == 'Child_Tracker_Eyesight':
                                feature_obj.Child_Tracker_Eyesight = False
                                feature_obj.save()
                            if j == 'Child_Tracker_Vaccination':
                                feature_obj.Child_Tracker_Vaccination = False
                                feature_obj.save()
                            if j == 'Child_Tracker_Food_and_Nutrition':
                                feature_obj.Child_Tracker_Food_and_Nutrition = False
                                feature_obj.save()
                            if j == 'Child_Tracker_Hand_and_Eye_Coordination':
                                feature_obj.Child_Tracker_Hand_and_Eye_Coordination = False
                                feature_obj.save()
                            if j == 'Child_Tracker_Learnability':
                                feature_obj.Child_Tracker_Learnability = False
                                feature_obj.save()
                            if j == 'Child_Tracker_Analytical':
                                feature_obj.Child_Tracker_Analytical = False
                                feature_obj.save()
                            if j == 'Child_Tracker_Motor_Skill':
                                feature_obj.Child_Tracker_Motor_Skill = False
                                feature_obj.save()
                            if j == 'Child_Tracker_Skin':
                                feature_obj.Child_Tracker_Skin = False
                                feature_obj.save()
                            if j == 'Child_Tracker_Hair':
                                feature_obj.Child_Tracker_Hair = False
                                feature_obj.save()
                            if j == 'Growth_Tracker_Child_Details':
                                feature_obj.Growth_Tracker_Child_Details = False
                                feature_obj.save()
                            if j == 'Growth_Tracker_View_Reports':
                                feature_obj.Growth_Tracker_View_Reports = False
                                feature_obj.save()
                            if j == 'Growth_Tracker_Testimonials':
                                feature_obj.Growth_Tracker_Testimonials = False
                                feature_obj.save()
                            if j == 'Eyesight_Tracker_Child_Details':
                                feature_obj.Eyesight_Tracker_Child_Details = False
                                feature_obj.save()
                            if j == 'Eyesight_Tracker_View_Reports':
                                feature_obj.Eyesight_Tracker_View_Reports = False
                                feature_obj.save()
                            if j == 'Eyesight_Tracker_Testimonials':
                                feature_obj.Eyesight_Tracker_Testimonials = False
                                feature_obj.save()
                            if j == 'Vaccination_Tracker_Child_Details':
                                feature_obj.Vaccination_Tracker_Child_Details = False
                                feature_obj.save()
                            if j == 'Vaccination_Tracker_View_Reports':
                                feature_obj.Vaccination_Tracker_View_Reports = False
                                feature_obj.save()
                            if j == 'Vaccination_Tracker_Testimonials':
                                feature_obj.Vaccination_Tracker_Testimonials = False
                                feature_obj.save()
                            if j == 'Food_Tracker_Child_Details':
                                feature_obj.Food_Tracker_Child_Details = False
                                feature_obj.save()
                            if j == 'Food_Tracker_Recommended_Meals':
                                feature_obj.Food_Tracker_Recommended_Meals = False
                                feature_obj.save()
                            if j == 'Food_Tracker_View_Reports':
                                feature_obj.Food_Tracker_View_Reports = False
                                feature_obj.save()
                            if j == 'Food_Tracker_Child_Testimonials':
                                feature_obj.Food_Tracker_Child_Testimonials = False
                                feature_obj.save()
                            if j == 'Hand_and_Eye_Tracker_Child_Details':
                                feature_obj.Hand_and_Eye_Tracker_Child_Details = False
                                feature_obj.save()
                            if j == 'Hand_and_Eye_Tracker_View_Reports':
                                feature_obj.Hand_and_Eye_Tracker_View_Reports = False
                                feature_obj.save()
                            if j == 'Hand_and_Eye_Tracker_Testimonials':
                                feature_obj.Hand_and_Eye_Tracker_Testimonials = False
                                feature_obj.save()
                            if j == 'Learnability_Tracker_Child_Details':
                                feature_obj.Learnability_Tracker_Child_Details = False
                                feature_obj.save()
                            if j == 'Learnability_Tracker_View_Reports':
                                feature_obj.Learnability_Tracker_View_Reports = False
                                feature_obj.save()
                            if j == 'Learnability_Tracker_Testimonials':
                                feature_obj.Learnability_Tracker_Testimonials = False
                                feature_obj.save()
                            if j == 'Analytical_Tracker_Child_Details':
                                feature_obj.Analytical_Tracker_Child_Details = False
                                feature_obj.save()
                            if j == 'Analytical_Tracker_View_Reports':
                                feature_obj.Analytical_Tracker_View_Reports = False
                                feature_obj.save()
                            if j == 'Analytical_Tracker_Testimonials':
                                feature_obj.Analytical_Tracker_Testimonials = False
                                feature_obj.save()
                            if j == 'Motor_Skill_Tracker_Child_Details':
                                feature_obj.Motor_Skill_Tracker_Child_Details = False
                                feature_obj.save()
                            if j == 'Motor_Skill_Tracker_View_Reports':
                                feature_obj.Motor_Skill_Tracker_View_Reports = False
                                feature_obj.save()
                            if j == 'Motor_Skill_Tracker_Testimonials':
                                feature_obj.Motor_Skill_Tracker_Testimonials = False
                                feature_obj.save()
                            if j == 'Skin_Tracker_Child_Details':
                                feature_obj.Skin_Tracker_Child_Details = False
                                feature_obj.save()
                            if j == 'Skin_Tracker_View_Reports':
                                feature_obj.Skin_Tracker_View_Reports = False
                                feature_obj.save()
                            if j == 'Skin_Tracker_Testimonials':
                                feature_obj.Skin_Tracker_Testimonials = False
                                feature_obj.save()
                            if j == 'Hair_Tracker_Child_Details':
                                feature_obj.Hair_Tracker_Child_Details = False
                                feature_obj.save()
                            if j == 'Hair_Tracker_View_Reports':
                                feature_obj.Hair_Tracker_View_Reports = False
                                feature_obj.save()
                            if j == 'Hair_Tracker_Testimonials':
                                feature_obj.Hair_Tracker_Testimonials = False
                                feature_obj.save()
                            if j == 'Consultation_Speciality':
                                feature_obj.Consultation_Speciality = False
                                feature_obj.save()
                            if j == 'Consultation_Search_Doctors':
                                feature_obj.Consultation_Search_Doctors = False
                                feature_obj.save()
                            if j == 'Consultation_Symptoms':
                                feature_obj.Consultation_Symptoms = False
                                feature_obj.save()
                            if j == 'Therapy_Speciality':
                                feature_obj.Therapy_Speciality = False
                                feature_obj.save()
                            if j == 'Therapy_Search_Doctors':
                                feature_obj.Therapy_Search_Doctors = False
                                feature_obj.save()
                            if j == 'Theraoy_Symptoms':
                                feature_obj.Theraoy_Symptoms = False
                                feature_obj.save()
                            if j == 'Subscription_Choose_Your_Subscription':
                                feature_obj.Subscription_Choose_Your_Subscription = False
                                feature_obj.save()
                            if j == 'Subscription_Membership':
                                feature_obj.Subscription_Membership = False
                                feature_obj.save()
                            if j == 'Subscription_Offers':
                                feature_obj.Subscription_Offers = False
                                feature_obj.save()
                            if j == 'Covid_Avoid_Covid':
                                feature_obj.Covid_Avoid_Covid = False
                                feature_obj.save()
                            if j == 'Covid_Symptoms':
                                feature_obj.Covid_Symptoms = False
                                feature_obj.save()
                            if j == 'Covid_Doctors':
                                feature_obj.Covid_Doctors = False
                                feature_obj.save()
                            if j == 'Covid_Screen_Time':
                                feature_obj.Covid_Screen_Time = False
                                feature_obj.save()
                            if j == 'Blogs_Trending_Blogs': 
                                feature_obj.Blogs_Trending_Blogs = False
                                feature_obj.save()
                            if j == 'Blogs_Categories':
                                feature_obj.Blogs_Categories = False
                                feature_obj.save()
                            if j == 'Blogs_Listing':
                                feature_obj.Blogs_Listing = False
                                feature_obj.save()
                            if j =='Kits_Categories':
                                feature_obj.Kits_Categories = False
                                feature_obj.save()
                            if j == 'Kits_Listing':
                                feature_obj.Kits_Categories = False
                                feature_obj.save()

                            # if j == 'home':
                            #     feature_obj.home = False
                            #     feature_obj.save()
                            # if j == 'growth_tracker':
                            #     feature_obj.growth_tracker = False
                            #     feature_obj.save()
                            # if j == 'eyesight_tracker':
                            #     feature_obj.eyesight_tracker = False
                            #     feature_obj.save()
                            # if j == 'vaccination_tracker':
                            #     feature_obj.vaccination_tracker = False
                            #     feature_obj.save()
                            # if j == 'food_nutrition_tracker':
                            #     feature_obj.food_nutrition_tracker = False
                            #     feature_obj.save()
                            # if j == 'hand_eye_tracker':
                            #     feature_obj.hand_eye_tracker = False
                            #     feature_obj.save()
                            # if j == 'learnability_tracker':
                            #     feature_obj.learnability_tracker = False
                            #     feature_obj.save()
                            # if j == 'analytical_tracker':
                            #     feature_obj.analytical_tracker = False
                            #     feature_obj.save()
                            # if j == 'motorskill_tracker':
                            #     feature_obj.motorskill_tracker = False
                            #     feature_obj.save()
                            # if j == 'skin_tracker':
                            #     feature_obj.skin_tracker = False
                            #     feature_obj.save()
                            # if j == 'hair_tracker':
                            #     feature_obj.hair_tracker = False
                            #     feature_obj.save()
                            # if j == 'consultation':
                            #     feature_obj.consultation = False
                            #     feature_obj.save()
                            # if j == 'therapy':
                            #     feature_obj.therapy = False
                            #     feature_obj.save()
                            # if j == 'subscription':
                            #     feature_obj.subscription = False
                            #     feature_obj.save()
                            # if j == 'covid_19':
                            #     feature_obj.covid_19 = False
                            #     feature_obj.save()
                            # if j == 'blogs':
                            #     feature_obj.blogs = False
                            #     feature_obj.save()
                            # if j == 'child_kits':
                            #     feature_obj.child_kits = False
                            #     feature_obj.save()
                            # if j == 'contact':
                            #     feature_obj.contact = False
                            #     feature_obj.save()
                        except Exception as e:
                            print(e)
                    return Response({"message": "Feature updated successfully"}, status=HTTP_200_OK)
                except Exception as e:
                    return Response({"message": str(e)}, status=HTTP_400_BAD_REQUEST)
            return Response({"message": serializer.errors}, status=HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "You are not authorized to perform this action"}, status=HTTP_400_BAD_REQUEST)