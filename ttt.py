def create_doctor(data):
    try:
        email = data.get('email')
        password = data.get('password')

        keys_to_convert = [
            'hospital_id',
            'roles',
            'speciality_id',
            'hospital_speciality_id',
            'scribe_id',  # This will now be a list of IDs
        ]

        data = convert_keys_to_object_id(data, keys_to_convert)

        hospital_id = data.get('hospital_id')
        hospital_speciality_id = data.get('hospital_speciality_id', '')
        speciality_id = data.get('speciality_id')
        doctor_default_timezone = data['doctor_timezone']
        doctor_hybrid_model = data['doctor_hybrid_model']
        upload_allowed = data['upload_allowed']
        teams_integration = data['teams_integration']
        scribe_ids = data.get('scribe_id', []) if doctor_hybrid_model else []

        # Validate hospital
        is_hospital_exists_and_active = hospital_manager.is_hospital_exists_by_id_and_is_active(hospital_id)
        if not is_hospital_exists_and_active:
            return error_processor('Hospital is not available or not active. Kindly add the hospital and try again.', 404)
        hospital = is_hospital_exists_and_active

        # Validate speciality
        is_speciality_exist_and_active = speciality_manager.is_speciality_exists_by_id_and_is_active(speciality_id)
        if not is_speciality_exist_and_active:
            return error_processor('Speciality is not available or not active. Kindly add the speciality and try again.', 404)
        speciality = is_speciality_exist_and_active

        # Validate template
        if not speciality['templates']:
            return error_processor('Template is not attached to this speciality. Please create and add a Template for the speciality first to proceed further', 404)
        template_id = string_to_object_id(speciality['templates']['template_id'])
        template = template_manager.get_template_by_id(template_id)
        if not template:
            return error_processor('Template is not attached to this speciality. Please create and add a Template for the speciality first to proceed further', 404)

        # Validate hospital speciality if provided
        hospital_speciality_to_be_inserted = {}
        if hospital_speciality_id:
            is_hospital_speciality_exist_and_active = hospital_speciality_manager.is_hospital_speciality_exist_and_active(hospital_speciality_id)
            if not is_hospital_speciality_exist_and_active:
                return error_processor('Hospital speciality is not available or not active. Kindly add the Hospital speciality and try again.', 404)
            hospital_speciality = is_hospital_speciality_exist_and_active
            hospital_speciality_to_be_inserted = {
                'hospital_speciality_id': hospital_speciality_id,
                'hospital_speciality_name': hospital_speciality['hospital_speciality_name'],
            }

        # Check if doctor email already exists
        is_doctor_exists = user_manager.is_user_exists_by_email(email)
        if is_doctor_exists:
            message = 'This email is already taken. Please try again with a different email'
            return already_exists(message)

        # Validate and prepare scribes
        scribes_to_be_inserted = []
        if doctor_hybrid_model and not scribe_ids:
            return error_processor('Scribe IDs list is empty. Kindly send at least one scribe ID.', 404)

        for scribe_id in scribe_ids:
            is_scribe_exists_and_active = user_manager.is_user_exists_by_id_and_is_active(scribe_id)
            if not is_scribe_exists_and_active:
                return error_processor(f'Scribe with ID {scribe_id} is not available or not active. Kindly add the scribe and try again.', 404)
            scribe = is_scribe_exists_and_active
            scribes_to_be_inserted.append({
                'scribe_id': scribe_id,
                'scribe_name': scribe['name'],
            })

        # Prepare doctor data
        doctor_data = {
            'name': data['name'],
            'email': email,
            'password': generate_password_hash(password, 14),
            'roles': [
                {
                    'role_id': string_to_object_id(data.get('roles')[0]),
                    'role_name': role_manager.get_role_by_id(string_to_object_id(data.get('roles')[0]))['role_name'],
                }
            ],
            'doctor': {
                'hospitals': [
                    {
                        'hospital_id': hospital_id,
                        'hospital_name': is_hospital_exists_and_active['hospital_name'],
                        'hospital_code': is_hospital_exists_and_active['hospital_code'],
                    }
                ],
                'scribes': scribes_to_be_inserted,
                'specialities': [
                    {
                        'speciality_id': speciality_id,
                        'speciality_name': is_speciality_exist_and_active['speciality_name'],
                        'specialtiy_code': is_speciality_exist_and_active['speciality_code'],
                    }
                ],
                'hospital_specialities': [hospital_speciality_to_be_inserted] if hospital_speciality_id else [],
                'note_style': 'paragraph',
                'doctor_default_timezone': doctor_default_timezone,
                'doctor_hybrid_model': doctor_hybrid_model,
                'upload_allowed': upload_allowed,
                'teams_integration': teams_integration,
                'show_icd': False,  # Default value as per sample
                'show_ehr': False,  # Default value as per sample
            },
            'template_id': template_id,
            'scribe': {},
            'is_active': True,
            'created_at': get_current_time_in_utc(),
            'created_by': data['created_by'],
            'updated_at': None,
            'updated_by': None,
        }

        # Insert doctor
        inserted_doctor = user_manager.add_user(doctor_data)
        doctor_id = inserted_doctor['_id']

        # Create chat for each scribe
        for scribe_id in scribe_ids:
            chat_data = {
                'scribe_id': scribe_id,
                'doctor_id': ObjectId(doctor_id),
                'chat': [],
            }
            chat_manager.add_chat(chat_data)

        # Update related collections for each scribe
        for scribe in scribes_to_be_inserted:
            scribe_id = scribe['scribe_id']
            # Add doctor to hospital speciality
            hospital_speciality_manager.add_doctor_in_hospital_speciality(inserted_doctor, hospital_speciality_id)
            # Add scribe to hospital speciality
            hospital_speciality_manager.add_scribe_in_hospital_speciality(scribe, hospital_speciality_id)
            # Add doctor to hospital
            hospital_manager.add_doctor_inside_hospital_speciality_in_hospital(inserted_doctor, hospital_id, hospital_speciality_id)
            hospital_manager.add_doctor_in_hospital(inserted_doctor, hospital_id, scribe, hospital_speciality_id)
            # Add scribe to hospital
            hospital_manager.add_scribe_in_hospital(inserted_doctor, scribe, hospital_id)
            # Add doctor to speciality
            speciality_manager.add_doctor_in_speciality(inserted_doctor, speciality_id)
            # Add scribe to speciality
            speciality_manager.add_scribe_in_speciality(scribe, speciality_id)
            # Update scribe user
            user_manager.update_scribe_user_after_assigning_to_doctor(scribe_id, speciality, inserted_doctor, hospital)

        message = 'Doctor added successfully.'
        status_code = 201
        data = {'Doctor': inserted_doctor}
        return response_processor(message, status_code, data)

    except Exception as e:
        error = str(e)
        return error_processor(error, 500)