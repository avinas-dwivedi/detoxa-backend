# class SaveErx(generics.GenericAPIView):
#     serializer_class = eRxSerializer
#
#     def post(self, request, consultationId):
#         try:
#             id = int(consultationId)
#             consultationObj = Consultation.objects.get(id=id)
#         except ValueError:
#             raise ValidationError(_('Consultation ID must be Numeric'))
#         except Consultation.DoesNotExist:
#             raise ValidationError(_('Invalid Consultation ID'))
#
#         serialized = eRxSerializer(data=request.data)
#
#         if serialized.is_valid():
#             for key in serialized.validated_data:
#                 if isinstance(serialized.validated_data.get(key), list):
#                     for obj in serialized.validated_data.get(key):
#                         for obj_key in obj:
#                             if obj[obj_key] == '-':
#                                 obj[obj_key] = None
#                 elif serialized.validated_data.get(key) == '-':
#                     serialized.validated_data[key] = None
#
#             patientName = serialized.validated_data.get('patientName')
#             patientGender = serialized.validated_data.get('patientGender')
#             patientAge = serialized.validated_data.get('patientAge')
#             patientId = serialized.validated_data.get('patientId')
#
#             temperature = serialized.validated_data.get('temperature')
#             bp = serialized.validated_data.get('bp')
#             if bp:
#                 bpSys = bp.split("/")[0]
#                 if bpSys == '-':
#                     bpSys = None
#                 bpDia = bp.split("/")[1]
#                 if bpDia == '-':
#                     bpDia = None
#             else:
#                 bpSys = None
#                 bpDia = None
#
#             weight = serialized.validated_data.get('weight')
#             height = serialized.validated_data.get('height')
#             lmp = serialized.validated_data.get('lmp')
#             followUp = serialized.validated_data.get('followUp')
#             if followUp:
#                 try:
#                     followUp = datetime.strptime(followUp, date_format.time_format4)
#                     followUp = followUp.date()
#                 except ValueError:
#                     raise ValidationError(_('followUp must be of format YYYY-MM-DD'))
#
#             adviceRemarks = serialized.validated_data.get('advice')
#             statusErx = 'Draft'
#             symptomsList = serialized.validated_data.get('symptomsList')
#             symptoms_List = []
#             hopi_list = []
#             for symptom in symptomsList:
#                 symptomName = symptom['symptomName']
#                 if symptomName is not None:
#                     symptoms_List.append(symptomName)
#                 hopi = symptom['hopi']
#                 if hopi is not None:
#                     hopi_list.append(hopi)
#             final_symptoms = str('^ '.join(symptoms_List))
#             final_hopi = str('^ '.join(hopi_list))
#
#             diagnosisList = serialized.validated_data.get('diagnosisList')
#             diagnosis_List = []
#             for diagnosis in diagnosisList:
#                 diagnosisName = diagnosis['diagnosisName']
#                 diagnosis_List.append(diagnosisName)
#             Temp_diagnosis_List = diagnosis_List
#
#             testList = serialized.validated_data.get('testList')
#             test_List = []
#             instruction_list = []
#             for test in testList:
#                 testName = test['testName']
#                 test_List.append(testName)
#                 instruction = test['testInstructions']
#                 instruction_list.append(instruction)
#             Temp_test_List = test_List
#             Temp_instruction_list = instruction_list
#
#             medicineList = serialized.validated_data.get('medicineList')
#             medicineName_List = []
#             strength_List = []
#             dosageForm_List = []
#             frequency_List = []
#             prePostMeal_List = []
#             duration_List = []
#             medicineInstruction_List = []
#             for medicine in medicineList:
#                 medicineName = medicine['medicineName']
#                 medicineName_List.append(medicineName)
#                 strength = medicine['strength']
#                 strength_List.append(strength)
#                 dosageForm = medicine['dosageForm']
#                 dosageForm_List.append(dosageForm)
#                 frequency = medicine['frequency']
#                 frequency_List.append(frequency)
#                 prePostMeal = medicine['prePostMeal']
#                 prePostMeal_List.append(prePostMeal)
#                 duration = medicine['duration']
#                 duration_List.append(duration)
#                 medicineInstruction = medicine['medicineInstruction']
#                 medicineInstruction_List.append(medicineInstruction)
#             Temp_medicineName_List = medicineName_List
#             Temp_strength_List = strength_List
#             Temp_dosageForm_List = dosageForm_List
#             Temp_frequency_List = frequency_List
#             Temp_prePostMeal_List = prePostMeal_List
#             Temp_duration_List = duration_List
#             Temp_medicineInstruction_List = medicineInstruction_List
#
#             if consultationObj.id is not None:
#                 eprescriptionObjs = Eprescription.objects.filter(consultation_id=consultationObj.id)
#                 if eprescriptionObjs.count() > 0:
#                     eprescriptionObj = Eprescription.objects.filter(consultation_id=consultationObj.id)
#                     eprescriptionObj.update(consultation_id=consultationObj, patient_id=patientId,
#                                             patient_name=patientName,
#                                             patient_age=patientAge, patient_gender=patientGender,
#                                             temperature=temperature,
#                                             weight=weight, patient_height=height, lmp=lmp, bp_sys=bpSys, bp_dia=bpDia,
#                                             chief_complaint_or_symptoms=final_symptoms, hopi=final_hopi,
#                                             advice=adviceRemarks,
#                                             follow_up_date=followUp, status=statusErx)
#                 else:
#                     Eprescription.objects.create(consultation_id=consultationObj, patient_id=patientId,
#                                                  patient_name=patientName,
#                                                  patient_age=patientAge, patient_gender=patientGender,
#                                                  temperature=temperature,
#                                                  weight=weight, patient_height=height, lmp=lmp, bp_sys=bpSys,
#                                                  bp_dia=bpDia,
#                                                  chief_complaint_or_symptoms=final_symptoms, hopi=final_hopi,
#                                                  advice=adviceRemarks,
#                                                  follow_up_date=followUp, status=statusErx)
#
#                 eprescriptionObj = Eprescription.objects.filter(consultation_id=consultationObj.id).first()
#
#                 ######################################################################################################
#                 eprescriptionDiagnosisObjs = EprescriptionDiagnosis.objects.filter(eprescription_id=eprescriptionObj.id)
#                 db_diagnosis_count = eprescriptionDiagnosisObjs.count()
#                 if db_diagnosis_count > 0:
#                     indx = 0
#                     for eprescriptionDiagnosisObj in eprescriptionDiagnosisObjs:
#                         no_of_diagnosis = len(Temp_diagnosis_List)
#                         if indx < no_of_diagnosis:
#                             diagnosisName = Temp_diagnosis_List[indx]
#                         eprescriptionDiagnosisUpdateObj = EprescriptionDiagnosis.objects.filter(
#                             id=eprescriptionDiagnosisObj.id)
#                         eprescriptionDiagnosisUpdateObj.update(eprescription_id=eprescriptionObj,
#                                                                diagnosis_or_provisional_diagnosis=diagnosisName)
#                         indx += 1
#                     if no_of_diagnosis > db_diagnosis_count:
#                         dbd = db_diagnosis_count
#                         for diagnosis in diagnosisList:
#                             if dbd < no_of_diagnosis:
#                                 diagnosisName = diagnosisList[dbd].get('diagnosisName')
#                                 EprescriptionDiagnosis.objects.create(eprescription_id=eprescriptionObj,
#                                                                       diagnosis_or_provisional_diagnosis=diagnosisName)
#                                 dbd += 1
#
#                 else:
#                     for diagnosis in diagnosisList:
#                         diagnosisName = diagnosis['diagnosisName']
#                         EprescriptionDiagnosis.objects.create(eprescription_id=eprescriptionObj,
#                                                               diagnosis_or_provisional_diagnosis=diagnosisName)
#
#                 ######################################################################################################
#                 eprescriptionInvestigationObjs = EprescriptionInvestigation.objects.filter(
#                     eprescription_id=eprescriptionObj.id)
#                 db_investigate_count = eprescriptionInvestigationObjs.count()
#                 if db_investigate_count > 0:
#                     indx_i = 0
#                     for eprescriptionInvestigationObj in eprescriptionInvestigationObjs:
#                         no_of_investigations = len(Temp_test_List)
#                         if indx_i < db_investigate_count:
#                             testName = Temp_test_List[indx_i]
#                             instrunctions = Temp_instruction_list[indx_i]
#                         eprescriptionInvestigationUpdateObj = EprescriptionInvestigation.objects.filter(
#                             id=eprescriptionInvestigationObj.id)
#                         eprescriptionInvestigationUpdateObj.update(eprescription_id=eprescriptionObj,
#                                                                    test_name=testName, instructions=instrunctions)
#                         indx_i += 1
#
#                     if no_of_investigations > db_investigate_count:
#                         dbic = db_investigate_count
#                         for test in testList:
#                             if dbic < no_of_investigations:
#                                 testName = testList[dbic].get('testName')
#                                 instructions = testList[dbic].get('testInstructions')
#                                 EprescriptionInvestigation.objects.create(eprescription_id=eprescriptionObj,
#                                                                           test_name=testName,
#                                                                           instructions=instructions)
#                                 dbic += 1
#
#                 else:
#                     i = 0
#                     for test in testList:
#                         testName = test['testName']
#                         if i < len(instruction_list):
#                             instructions = instruction_list[i]
#                         EprescriptionInvestigation.objects.create(eprescription_id=eprescriptionObj, test_name=testName,
#                                                                   instructions=instructions)
#                         i += 1
#
#                 ######################################################################################################
#                 eprescriptionMedicineObjs = EprescriptionMedicine.objects.filter(eprescription_id=eprescriptionObj.id)
#                 db_medicine_count = eprescriptionMedicineObjs.count()
#                 if db_medicine_count > 0:
#                     indx_m = 0
#                     for eprescriptionMedicineObj in eprescriptionMedicineObjs:
#                         if indx_m < db_medicine_count:
#                             medicineName = Temp_medicineName_List[indx_m]
#                             strength = Temp_strength_List[indx_m]
#                             dosageForm = Temp_dosageForm_List[indx_m]
#                             frequency = Temp_frequency_List[indx_m]
#                             prePostMeal = Temp_prePostMeal_List[indx_m]
#                             if prePostMeal == True:
#                                 prePostMeal = 'Before Food'
#                             else:
#                                 prePostMeal = 'After Food'
#                             duration = Temp_duration_List[indx_m]
#                             medicineInstruction = Temp_medicineInstruction_List[indx_m]
#                         eprescriptionMedicineUpdateObj = EprescriptionMedicine.objects.filter(
#                             id=eprescriptionMedicineObj.id)
#                         eprescriptionMedicineUpdateObj.update(eprescription_id=eprescriptionObj,
#                                                               medicine=medicineName, strength=strength,
#                                                               dosage_form=dosageForm, frequency=frequency,
#                                                               prepost_meal=prePostMeal, duration=duration,
#                                                               other_instructions=medicineInstruction)
#                         indx_m += 1
#
#                     if len(Temp_medicineName_List) > db_medicine_count:
#                         dbi = db_medicine_count
#                         for medicine in medicineList:
#                             if dbi < len(medicineName_List):
#                                 medicineName = medicineName_List[dbi]
#                                 strength = strength_List[dbi]
#                                 dosageForm = dosageForm_List[dbi]
#                                 frequency = frequency_List[dbi]
#                                 prePostMeal = prePostMeal_List[dbi]
#                                 if prePostMeal == True:
#                                     prePostMeal = 'Before Food'
#                                 else:
#                                     prePostMeal = 'After Food'
#                                 duration = duration_List[dbi]
#                                 medicineInstruction = medicineInstruction_List[dbi]
#
#                                 EprescriptionMedicine.objects.create(eprescription_id=eprescriptionObj,
#                                                                      medicine=medicineName, strength=strength,
#                                                                      dosage_form=dosageForm, frequency=frequency,
#                                                                      prepost_meal=prePostMeal, duration=duration,
#                                                                      other_instructions=medicineInstruction)
#                                 dbi += 1
#                 else:
#                     ii = 0
#                     for medicine in medicineList:
#                         medicineName = medicine['medicineName']
#                         if ii < len(medicineName_List):
#                             strength = strength_List[ii]
#                             dosageForm = dosageForm_List[ii]
#                             frequency = frequency_List[ii]
#                             prePostMeal = prePostMeal_List[ii]
#                             if prePostMeal == True:
#                                 prePostMeal = 'Before Food'
#                             else:
#                                 prePostMeal = 'After Food'
#                             duration = duration_List[ii]
#                             medicineInstruction = medicineInstruction_List[ii]
#
#                             ii += 1
#
#                             EprescriptionMedicine.objects.create(eprescription_id=eprescriptionObj,
#                                                                  medicine=medicineName, strength=strength,
#                                                                  dosage_form=dosageForm, frequency=frequency,
#                                                                  prepost_meal=prePostMeal, duration=duration,
#                                                                  other_instructions=medicineInstruction)
#
#             return Response(status=status.HTTP_200_OK)
#         else:
#             return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
