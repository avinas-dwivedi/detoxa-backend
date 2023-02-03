"""detoxa_backend URL Configuration"""

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from detoxa_services.views import favourites_views, feature_views, food_nutrition_views, meals, notification, promocode_views

from .views import user_registration, user_login_with_password, \
    user_login_with_mobile_otp, media, blog, testimonials, banners,\
    child_tracker, lernability_tracker, eye_sight_tracker, hand_eye_tracker, vaccination, \
    contact_us, user_children, doctors_views, appointments, promocode_views, feedbacks_views, \
    reports_views, doctors, subscription_views, kit_views, organizations_views, hospital_views, motor_skills_views, \
    analytical_tracker, hair_tracker, skin_tracker, therapy, therapy_session, address_views,order_views, country_views


urlpatterns = [
    # User
    path('auth/user/register/create-otp/',
         user_registration.UserRegistrationCreateOTP.as_view(), name='UserRegistrationCreateOTP'),
    path('auth/user/register', user_registration.UserRegistration.as_view(),
         name='UserRegistration'),
    path('manage/admin/add', user_registration.AdminRegistration.as_view(),
         name='AdminRegistration'),
    path('auth/user/generateSignInOtp',
         user_login_with_mobile_otp.GenerateSignInOTP.as_view(), name='GenerateSignInOtp'),
    path('auth/user/login/withpassword', user_login_with_password.UserSignInWithPassword.as_view(),
         name='UserLoginInWithPassword'),
    path('auth/user/login/passwordless',
         user_login_with_mobile_otp.UserSignInWithOTP.as_view(), name='UserSignInWithOTP'),
    path('auth/user/signout',
         user_login_with_password.UserSignOut.as_view(), name='UserSignOut'),
    path('auth/user/update/<int:pk>/',
         user_registration.UpdateUser.as_view(), name='UpdateUser'),
    path('auth/user/update/password/<int:pk>/',
         user_registration.ChangePasswordAPIView.as_view(), name='ChangePasswordAPIView'),
    path('auth/user/reset-password/',
         user_registration.UserForgotPassword.as_view(), name='UserForgotPassword'),
    path('auth/user/delete-users/<int:pk>/',
         user_registration.DeleteUser.as_view(), name='DeleteUser'),
    # Media
    path('manage/admin/media', media.MediaUpload.as_view(), name='UploadMedia'),
    path('manage/admin/media/mediacategory',
         media.AddMediaCategory.as_view(), name='AddMediaCategory'),
    path('public/media/mediacategories',
         media.GetAllMediaCategory.as_view(), name='GetAllMediaCategory'),
    path('public/media', media.GetAllMedia.as_view(), name='GetAllMedia'),
    path('public/media/<int:pk>', media.GetMediaById.as_view(), name='GetMediaById'),
    path('manage/admin/media/<int:pk>',
         media.RemoveMedia.as_view(), name='RemoveMedia'),
     path('manage/admin/get-all-users/',user_registration.GetUsersAPIView.as_view(),name='GetAllUsers'),


    # Blog
    path('manage/admin/blog', blog.CreateBlog.as_view(), name='CreateBlog'),
    path('manage/admin/blog/blogcategory',
         blog.AddBlogCategory.as_view(), name='AddBlogCategory'),
    path('public/blog/blogcategories',
         blog.GetAllBlogCategory.as_view(), name='GetAllBlogCategory'),
    path('public/blog/authors', blog.GetAllAuthors.as_view(), name='GetAllAuthors'),
    path('public/blog/blog-by-category/<str:category>',
         blog.BlogByCategory.as_view(), name='GetBlogByCategory'),
    path('public/blog/most-viewed-blogs',
         blog.MostViewedBlogs.as_view(), name='MostViewedBlogs'),
    path('public/blog', blog.GetAllBlogs.as_view(), name='GetAllblogs'),
    path('public/blog/<int:pk>', blog.GetBlogById.as_view(), name='GetBlogById'),
    path('manage/admin/blog/<int:pk>',blog.RemoveBlog.as_view(), name='RemoveBlog'),
    path('manage/admin/update-blog-details/<int:pk>',blog.UpdateBlogDetails.as_view(), name='UpdateBlogDetails'),
    path('manage/delete-blog-category/<int:pk>/', blog.DeleteBlogCategory.as_view(), name='DeleteBlogCategory'),



    # Testimonial
    path('manage/admin/testimonial',
         testimonials.AddTestimonial.as_view(), name='AddTestimonial'),
    path('public/testimonials/AllTestimonials',
         testimonials.GetAllTestimonials.as_view(), name='AllTestimonials'),
    path('public/testimonials/<int:pk>',
         testimonials.GetTestimonialById.as_view(), name='GetTestimonialById'),
    path('manage/admin/testimonials/<int:pk>',
         testimonials.RemoveTestimonial.as_view(), name='RemoveTestimonial'),
    path('manage/admin/testimonials/services',
         testimonials.AddService.as_view(), name='AddService'),
    path('public/testimonials/services',
         testimonials.GetAllServices.as_view(), name='GetAllServices'),
    path('manage/admin/testimonials/services/<int:pk>',
         testimonials.RemoveService.as_view(), name='RemoveService'),

    # Banner
    path('manage/admin/banner', banners.AddBanner.as_view(), name='AddBanner'),
    path('public/banner/AllBanners',
         banners.GetAllBanners.as_view(), name='GetAllBanners'),
    path('public/banner/<int:pk>',
         banners.GetBannerById.as_view(), name='GetBannerById'),
    path('manage/admin/banner/<int:pk>',
         banners.RemoveBanner.as_view(), name='RemoveBanner'),

    # Growth tracker
    path('growth-tracker/user/growth-tracker',
         child_tracker.ChildTrackerView.as_view(), name='ChildTracker'),
    path('growth-tracker/user/get-growth-tracker',
         child_tracker.GetAllChildTrackerById.as_view(), name='GetAllChildTracker'),


    # Eye sight tracker
    path('eye-sight-tracker/user/eyesight-tracker',
         eye_sight_tracker.EyeSightTrackerView.as_view(), name='EyeSightTrackerView'),
    path('eye-sight-tracker/user/get-eyesight-tracker',
         eye_sight_tracker.EyeSightTrackerListView.as_view(), name='EyeSightTrackerListView'),

    # Hand Eye tracker
    path('hand-eye-tracker/user/handeye-tracker',
         hand_eye_tracker.HandEyeTrackerView.as_view(), name='HandEyeTrackerView'),
    path('hand-eye-tracker/user/get-handeye-tracker-report/',
         hand_eye_tracker.GetHandEyeTrackerView.as_view(), name='GetHandEyeTrackerView'),


    # Learnability tracker
    path('learnability-tracker/user/add/data', lernability_tracker.LearnabilityTrackerView.as_view(),
         name='LearnabilityTrackerView'),
    path('learnability-tracker/user/get/data', lernability_tracker.GetLearnablityTracker.as_view(),
         name='GetLearnablityTracker'),

    # Food and Nutrition Tracker
    path('food-nutrition-tracker/user/add/data',
         food_nutrition_views.FoodNutritionAPIView.as_view(), name='FoodNutritionAPIView'),
    path('food-nutrition-tracker/get-recommended-meals',
         meals.RecommendedMealsView.as_view(), name='RecommendedMealsView'),
    path('food-nutrition-tracker/get-recommended-meals-details/<int:pk>/',
         meals.RecommendedMealsDetailsView.as_view(), name='RecommendedMealsDetailsView'),
     path('food-nutrition-tracker/add-meals',meals.AddMealsView.as_view(),name='AddMealsView'),

    # analytical tracker
    path('analytical-tracker/user/analytical_tracker', analytical_tracker.AnalyticalTrackerView.as_view(),
         name='AnalyticalTrackerView'),

    # Vaccination
    path('vaccination/data/add',
         vaccination.AddVaccineData.as_view(), name='AddVaccineData'),
    path('vaccination/data/get', vaccination.GetAllVaccineByAgeGroup.as_view(),
         name='GetVaccineDataByAgeGroup'),
    path('vaccination/update-status/',
         vaccination.VaccineMarkDone.as_view(), name='VaccineMarkDone'),
    path('vaccination/set-reminder/',
         vaccination.SetVaccineReminderView.as_view(), name='SetReminderVaccine'),
    path('vaccination/cancel-vaccination-appointment/<int:pk>/',
         vaccination.CancelVaccinationAppointmentView.as_view(), name='CancelVaccinationAppointmentView'),
    path('vaccination/book-vaccination-appointment/',
         vaccination.BookVaccinationAppointment.as_view(), name='BookVaccinationAppointment'),
    # Motor SKill
    path('motor-skill/user/add/data/',
         motor_skills_views.MotorSkillTrackerView.as_view(), name='MotorSkillTrackerView'),
    path('motor-skill/user/get/data/',
         motor_skills_views.GetMotorSkillTracker.as_view(), name='GetMotorSkillTracker'),
    # Contact us
    path('contact-us/create', contact_us.ContactUsView.as_view(), name='AddContactUs'),

    # Add Children
    path('user/child', user_children.AddChildUser.as_view(), name='AddUserChild'),
    path('user/child/update/<int:pk>/',
         user_children.UpdateUserChild.as_view(), name='UpdateUserChild'),
    path('user/child/delete/<int:pk>/',
         user_children.DeleteUserChild.as_view(), name='DeleteUserChild'),
    path('user/child/details/<int:pk>/',
         user_children.GetChildrenDetails.as_view(), name='GetChildrenDetails'),

    # Doctors
    path('doctors/get-doctors/',
         doctors_views.GetDoctorsView.as_view(), name='GetDoctorsView'),
    path('doctors/create-doctor/',
         doctors_views.CreateDoctorsView.as_view(), name='CreateDoctorsView'),
    path('doctors/specialization/',
         doctors_views.DoctorSpecializationView.as_view(), name='DoctorSpecializationView'),
    # path('doctors/upload-image/',
    #         doctors_views.S3UploadView.as_view(), name='S3UploadView'),

    # Appointment
    path('appointment/create/', appointments.CreateNewAppointment.as_view(),
         name='CreateAppointment'),
    path('appointment/get-appointments/',
         appointments.GetAllAppointments.as_view(), name='GetAllAppointments'),
    path('appointment/update/<int:pk>/',
         appointments.UpdateAppointment.as_view(), name='UpdateAppointment'),
    #     path('appointment/cancel/<int:pk>/',
    #          appointments.CancelAppointment.as_view(), name='CancelAppointment'),


    # Promocode
    path('create_promo_code/', promocode_views.CreatePromoCodeAPI.as_view(),
         name='create_promo_code'),
    path('promocode/apply/', promocode_views.ApplyPromocode.as_view(),
         name='ApplyPromocode'),
    path('promocode/list/', promocode_views.GetPromocodes.as_view(),
         name='GetPromocodes'),
    # Feedback
    path('feedback/create/', feedbacks_views.CreateFeedbackView.as_view(),
         name='CreateFeedback'),

    # Reports
    path('report/download-learnability-report/', reports_views.CreateLearnabilityReportPDFView.as_view(),
         name='CreateLearnabilityReportPDFView'),
    path('report/download-growth-report/', reports_views.CreateGrowthReportPDFView.as_view(),
         name='CreateGrowthReportPDFView'),
    path('report/download-eyesight-report/', reports_views.CreateEyeSightReportPDFView.as_view(),
         name='CreateEyeSightReportPDFView'),
    path('report/download-coordination-report/', reports_views.CreateCoordinationReportPDFView.as_view(),
         name='CreateCoordinationReportPDFView'),
    path('report/download-motor-skill-report/', reports_views.CreateMotorSkillReportPDFView.as_view(),
         name='CreateMotorSkillReportPDFView'),
    path('report/get-reports/', reports_views.ReportListView.as_view(),
         name='ReportListView'),
    path('report/get-report-details/<int:pk>/',
         reports_views.GetReportsDetails.as_view(), name='GetReportsDetails'),
    path('report/get-latest-reports/', reports_views.GetLatestReportListView.as_view(),
         name='getLatestReportListView'),

    path('report/download-analytical-report/', reports_views.CreateAnalyticalReportPDFView.as_view(),
         name='CreateAnalyticalReportPDFView'),
    path('report/generate-report-otp/',
         reports_views.GenerateOTPforReport.as_view(), name='GenerateOTPforReport'),
    path('report/verify-report-otp/',
         reports_views.VerifyOTPforReport.as_view(), name='VerifyOTPforReport'),
    path('report/medical-report/', reports_views.GenerateMedicalReportCard.as_view(),
         name='GenerateMedicalReportCard'),
     path('report/get-medical-report/', reports_views.GetMedicalReportList.as_view(),name='GetMedicalReportList'),
     path('report/send-medical-report-on-email/', reports_views.SendMedicalReportOnEmail.as_view(),name='SendMedicalReportOnEmail'),
    # Bulk data creation
    path('bulk-data/create/', doctors_views.EnterInitialData.as_view(),
         name='EnterInitialData'),

    path('manage/admin/createDoctor',
         doctors.CreateNewDoctors.as_view(), name='createNewDoctors'),
    path('manage/admin/getDoctors',
         doctors.GetAllDoctors.as_view(), name='getAllDoctors'),
    path('manage/admin/createSpecialization',
         doctors.CreateSpecialization.as_view(), name='createSpecialization'),
    path('manage/admin/getAllSpecialization',
         doctors.GetAllSpecialization.as_view(), name='getAllSpecialization'),
    path('manage/admin/getDoctorsById/<int:pk>',
         doctors.GetDoctorsById.as_view(), name='getDoctorsById'),
    path('manage/admin/delete-doctor/<int:pk>',
         doctors.DeleteDoctors.as_view(), name='deleteDoctor'),
    path('manage/admin/update-doctor-details/<int:pk>',
         doctors.UpdateDoctorDetails.as_view(), name='UpdateDoctorDetails'),

    path('manage/admin/delete-doctor-specialization/<int:pk>/', doctors.DeleteSpecialization.as_view(),
         name='DeleteSpecialization'),

    # Transaction
    path('transaction/create/', subscription_views.CreateSubscriptionTransaction.as_view(),
         name='CreateSubscriptionTransaction'),
    path('transaction/update/', subscription_views.UpdateSubscriptionTransaction.as_view(),
         name='UpdateSubscriptionTransaction'),

    # Kits
    path('kits/kits-by-category/<int:pk>/',
         kit_views.GetKitList.as_view(), name='GetKitList'),
    path('kits/kits-categories/', kit_views.GetKitCategoryList.as_view(),
         name='GetKitCategoryList'),
    path('kits/kits-details/<int:pk>/',
         kit_views.GetKitDetail.as_view(), name='GetKitDetail'),
    path('kits/manage/admin/create-kit/',
         kit_views.CreateKit.as_view(), name='CreateKit'),
    path('kits/manage/admin/update-kit/<int:pk>/',
         kit_views.UpdateKit.as_view(), name='UpdateKit'),
    path('kits/manage/admin/all-kits/',
         kit_views.GetAllKits.as_view(), name='GetAllKits'),
     path('kits/manage/admin/delete-kit-category/<int:pk>/',kit_views.DeleteKitCategroy.as_view(),name='DeleteKitCategroy'),
     path('kits/manage/admin/delete-kit/<int:pk>/',kit_views.DeleteKit.as_view(),name='DeleteKit'),
     path('kits/manage/admin/add-kit-category/',kit_views.AddKitCategory.as_view(),name='AddKitCategory'),
    # Organization
    path('organization/manage/admin/create-organization/',
         organizations_views.CreateOrganizationView.as_view(), name='CreateOrganizationView'),
    path('organization/manage/admin/get-organizations/',
         organizations_views.GetOrganizationsListView.as_view(), name='GetOrganizationsListView'),
    path('organization/manage/admin/update-organizations/<int:pk>/',
         organizations_views.UpdateOrganization.as_view(), name='UpdateOrganization'),
    path('organization/manage/admin/create-organization-user/',
         organizations_views.CreateOrganizationUserAPIView.as_view(), name='CreateOrganizationUserAPIView'),
    path('organization/manage/admin/get-organization-user/',
         organizations_views.GetOrganizatonUsersList.as_view(), name='GetOrganizatonUsersList'),
    path('organization/manage/admin/delete-organization/<int:pk>/',
         organizations_views.DeleteOrganization.as_view(), name='DeleteOrganization'),
    path('organization/manage/admin/delete-organization-user/<int:pk>/',
         organizations_views.DeleteOrganizationUser.as_view(), name='DeleteOrganizationUser'),
    path('organization/manage/admin/get-organization-details/<int:pk>/',
         organizations_views.GetOrganizationDetailsAPIView.as_view(), name='GetOrganizationDetailsAPIView'),
    path('organization/manage/admin/get-organization-user-details/<int:pk>/',
         organizations_views.GetOrganizationUserDetailsAPIView.as_view(), name='GetOrganizationUserDetailsAPIView'),
    path('organization/manage/admin/update-organization-user-details/<int:pk>/',
         organizations_views.UpdateOrganizationUserDetails.as_view(), name='UpdateOrganizationUserDetails'),
    # Hospital
    path('hospital/manage/admin/create-hospital/',
         hospital_views.CreateHospitalView.as_view(), name='CreateHospitalView'),
    path('hospital/manage/admin/create-hospital-user/',
         hospital_views.CreateHospitalUser.as_view(), name='CreateHospitalUser'),
    path('hospital/manage/admin/get-hospitals/',
         hospital_views.GetHospitalListView.as_view(), name='GetHospitalListView'),
    path('hospital/manage/admin/get-hospital-users/',
         hospital_views.GetHospitalUsers.as_view(), name='GetHospitalUsers'),
    path('hospital/manage/admin/update-hospital/<int:pk>/',
         hospital_views.UpdateHospital.as_view(), name='UpdateHospital'),
    path('hospital/manage/admin/delete-hospital/<int:pk>/',
         hospital_views.DeleteHospital.as_view(), name='DeleteHospital'),
    path('hospital/manage/admin/delete-hospital-user/<int:pk>/',
         hospital_views.DeleteHospitalUser.as_view(), name='DeleteHospitalUser'),
    path('hospital/manage/admin/get-hospital-detail/<int:pk>/',
         hospital_views.GetHospitalDetail.as_view(), name='GetHospitalDetail'),
    path('hospital/manage/admin/get-hospital-user-detail/<int:pk>/',
         hospital_views.GetHospitalUserDetail.as_view(), name='GetHospitalUserDetail'),
    path('hospital/manage/admin/update-hospital-user-detail/<int:pk>/',
         hospital_views.UpdateHospitalUser.as_view(), name='UpdateHospitalUser'),

    # Count
    path('count/get-count/',
         organizations_views.GetTotalsCount.as_view(), name='GetCount'),
    path('count/get-count-per-entity-type/',
         organizations_views.GetTotalsCountPerMonth.as_view(), name='GetCount'),
    # path('image-upload/',doctors_views.S3UploadView.as_view(), name='S3UploadView'),

    # skin tracker
    path('skin-tracker/user/add/data',
         skin_tracker.SkinTrackerView.as_view(), name='SkinTrackerView'),
    path('skin-tracker/user/get/data',
         skin_tracker.GetSkinTracker.as_view(), name='GetSkinTracker'),

    path('report/download-skin-report/',
         reports_views.CreateSkinReportPDFView.as_view(), name='CreateSkinReportPDFView'),

    # hair tracker
    path('hair-tracker/user/add/data',
         hair_tracker.HairTrackerView.as_view(), name='HairTrackerView'),
    path('hair-tracker/user/get/data',
         hair_tracker.GetHairTracker.as_view(), name='GetHairTracker'),

    path('report/download-hair-report/',
         reports_views.CreateHairReportPDFView.as_view(), name='CreateHairReportPDFView'),


    # super admin
    path('super-admin/manage/admin/create-super-admin-notifications/',
         notification.CreateNotifications.as_view(), name='CreateNotifications'),
    path('super-admin/manage/admin/update-super-admin-notifications/<int:pk>/',
         notification.UpdateNotifications.as_view(), name='UpdateNotifications'),
    path('super-admin/manage/admin/delete-super-admin-notifications/<int:pk>/',
         notification.DeleteNotifications.as_view(), name='DeleteNotifications'),

    path('super-admin/manage/admin/get-super-admin-notifications_WithID/<int:pk>/',
         notification.NotificationGetView.as_view(), name='NotificationGetView'),
    path('super-admin/manage/admin/get-super-admin-notifications/',
         notification.NotificationListView.as_view(), name='NotificationListView'),
    path('super-admin/manage/admin/send-super-admin-notifications/',
         notification.SendNotificationsForExistingUser.as_view(), name='SendNotificationsForExistingUser'),
    path('super-admin/manage/admin/send-super-admin-excel-sheet-notifications/',
         notification.SendNotificationsExcelSheet.as_view(), name='SendNotificationsExcelSheet'),
    path('super-admin/manage/admin/make-user-admin/',
         notification.MakeUserAdminApiView.as_view(), name='MakeUserAdminApiView'),

    # Therapist API

    path('manage/admin/createTherapist',
         therapy.CreateNewTherapist.as_view(), name='createNewDoctors'),
    path('manage/admin/getTherapist',
         therapy.GetAllTherapist.as_view(), name='getAllTherapist'),
    path('manage/admin/createTherapyCategory', therapy.CreateTherapyCategory.as_view(), name='createTherapyCategory'),
    path('manage/admin/getAllTherapistCategory',
         therapy.GetAllTherapistCategory.as_view(), name='getAllTherapistCategory'),

    path('manage/admin/delete-therapist-category/<int:pk>',
         therapy.DeleteTherapistCategory.as_view(), name='deletetherapistcategory'),
    path('manage/admin/getTherapistById/<int:pk>',
         therapy.GetTherapistById.as_view(), name='getTherapistById'),
    path('manage/admin/delete-therapist/<int:pk>',
         therapy.DeleteTherapist.as_view(), name='deleteDoctor'),
    path('manage/admin/update-therapist-details/<int:pk>', therapy.UpdateTherapistDetails.as_view(),
         name='UpdateTherapistDetails'),

    # Appointment
    path('therapy-session/create/', therapy_session.CreateNewTherapySession.as_view(),
         name='CreateAppointment'),
    path('therapy-session/get-therapy-session/',
         therapy_session.GetAllTherapySession.as_view(), name='GetAllTherapySession'),
    path('therapy-session/update/<int:pk>/',
         therapy_session.UpdateTherapySession.as_view(), name='UpdateTherapySession'),

     ### Favourites ###
     path('favourites/mark-favourite/', favourites_views.AddFavouritesView.as_view(), name='AddFavouritesView'),
     # path('favourites/un-mark-favourite/', favourites_views.RemoveFavourite.as_view(), name='RemoveFavourite'),
     path('favourites/get-favourites/', favourites_views.FavouritesListView.as_view(), name='FavouritesListView'),


     ### Address ###
     path('address/create/', address_views.AddAddressView.as_view(), name='AddAddressView'),
     path('address/get-addresses/', address_views.AddressListView.as_view(), name='AddressListView'),
     path('address/update/<int:pk>/', address_views.UpdateAddressView.as_view(), name='UpdateAddressView'),
     path('address/delete/<int:pk>/', address_views.DeleteAddressView.as_view(), name='DeleteAddressView'),
     path('address/get-address-by-id/<int:pk>/', address_views.GetAddressById.as_view(), name='GetAddressById'),
     
     ### Order ###
     path('order/create/', order_views.CreateOrderView.as_view(), name='CreateOrderView'),
     path('order/get-orders/', order_views.OrderListView.as_view(), name='OrderListView'),
     path('order/cancel/<int:pk>/', order_views.CancelOrdeView.as_view(), name='CancelOrdeView'),
     path('order/get-order-details/<int:pk>/', order_views.GetOrderById.as_view(), name='GetOrderById'),
     path('order/get-invoices/', order_views.GetInvoices.as_view(), name='GetInvoices'),
     
     ### Order Transaction ###
     path('order-transaction/create/', order_views.CreateOrderTransactionView.as_view(), name='CreateOrderTransactionView'),
     path('order-transaction/get-order-transactions/', order_views.OrderTransactionListView.as_view(), name='OrderTransactionListView'),
     path('order-transaction/get-order-transaction-details/<int:pk>/', order_views.GetOrderTransactionById.as_view(), name='GetOrderTransactionById'),

     ### Bank Details ###
     path('bank-details/create/', doctors.SaveBankDetails.as_view(), name='SaveBankDetails'),
     path('bank-details/update/<int:pk>/', doctors.UpdateBankDetails.as_view(), name='UpdateBankDetails'),

     ### Dashboard Details ###
     path('dashboard-details/',doctors.GetDashBoardDetails.as_view(),name='GetDashBoardDetails'),

     ### Order for admin ###
     path('order/get-orders-for-admin/', order_views.GetOrdersForAdmin.as_view(), name='GetOrdersForAdmin'),
     path('order/get-order-details-for-admin/<int:pk>/', order_views.GetOrderByIdForAdmin.as_view(), name='GetOrderByIdForAdmin'),
     path('order/update-order-for-admin/<int:pk>/', order_views.UpdateOrderStatusForAdmin.as_view(), name='GetOrderTransactionByIdForAdmin'),

     ### Features ###
     path('features/get/', feature_views.FeatureListView.as_view(), name='FeatureListView'),
     path('features/update/', feature_views.UpdateFeatureView.as_view(), name='UpdateFeatureView'),

     ### Cart ###
     path('cart/add-item/', order_views.AddItemToCart.as_view(), name='AddItemToCart'),
     path('cart/get-cart-item/', order_views.GetCartItems.as_view(), name='AddItemToCart'),
     path('cart/update-cart-item/<int:pk>/', order_views.UpdateCartItem.as_view(), name='UpdateCartItem'),
     path('cart/remove-cart-item/<int:pk>/', order_views.RemoveItemFromCart.as_view(), name='RemoveItemFromCart'),
     path('cart/get-cart-item-datails/<int:pk>/', order_views.GetCartItemDetails.as_view(), name='GetCartItemDetails'),
     path('cart/clear-cart-items', order_views.ClearCartAPIView.as_view(), name='ClearCartAPIView'),


    ### Country
    path('get-states-by-code/<str:code>/', country_views.CountryStatesView.as_view(), name='CountryStatesView'),
    path('get-country-by-name/<str:name>/', country_views.CountryView.as_view(), name='CountryView'),
    path('states/<int:pk>/', country_views.UploadVoiceView.as_view(), name='UploadVoiceView'),

    #### Animals
    path('get-animals-by-name/<str:name>/', country_views.GetAnimalsView.as_view(), name='GetAnimalsView'),
    path('get-vehicle-by-name/<str:name>/', country_views.GetVehiclesView.as_view(), name='GetVehiclesView'),
    path('get-profession-by-name/<str:name>/', country_views.GetProfessionView.as_view(), name='GetProfessionView'),
    path('get-solor-by-name/<str:name>/', country_views.GetSolarView.as_view(), name='GetSolarView'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
