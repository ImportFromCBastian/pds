from src.core.models import content


def create_contents():
    """
    Create a content.
    """
    content1 = content.create_content(
        titulo="Concurso Ecuestre Integrado #13",
        copete="Celebramos los 30 años de CEDICA",
        contenido="""Hola a tod@s!! el 17 de noviembre tendremos el CONCURSO ECUESTRE INTEGRADO, el #13!!! 
        Esta edición del CONCURSO viene con un plus muy especial ✨ ya que celebramos los 30 años de CEDICA 🤍 
        La entrada es abierta y gratuita, sólo completando un formulario de inscripción 🫶🏼
        Abajo, en los comentarios les dejamos el link para inscribirse!! 
        Como siempre estará nuestro Buffet con menú dulce y salado, bebidas frías y agua caliente para los mates!
        🍔🍕🥪🥐🍩🧁🧉🥤
        Y ya saben.. cualquier duda nos escriben!! 
        WhatsApp: +54 9 1167630247
        Gracias por acompañarnos 🤍🐎""",
        estado="Publicado",
        fecha_publicacion="2021-11-01",
        autor_email="aaaa@gmail.com"
    )

    content2 = content.create_content(
        titulo="Biomecánica de la Pelvis al Montar en Hipoterapia",
        copete="Clínica sobre la biomecánica de la pelvis en la rehabilitación física",
        contenido="""BIOMECANICA DE LA PELVIS AL MONTAR, COMO PRINCIPIO DE LA REHABILITACIÓN FISICA EN LA HIPOTERAPIA
        Esta Clínica te permitirá aprender, experimentar y trasladar los componentes Biomecánicos de la pelvis al montar en los tres aires, a la consecución de efectos terapéuticos en la rehabilitación de la discapacidad física.
        Descubrirás como la pelvis, -al ser una estructura fundamental en el desarrollo motor desde los primeros patrones de movimiento del ser humano hasta los patrones motores más complejos posteriores del neurodesarrollo-, establece la base de comunicación entre el cuerpo del jinete con discapacidad y el caballo, convirtiéndose en la puerta de entrada para la corrección estructural de otras funciones corporales necesarias para el movimiento.
        📍La primera parte-teórica- se dicta en el Edición Karakachoff de la Universidad Nacional de La Plata, el viernes 15 de noviembre, de 17 a 19 hs.
        📍La parte práctica de la clínica,-con participación activa de amazonas y jinetes montados-, se realizará el sábado 16 de noviembre en Campo Arroyo San Juan, sede de CEDICA en la localidad de Arturo Seguí, partido de La Plata, PBA, de 9:30 a 18:30 hs.
        Al finalizar habrá un buffet de campo 🧉
        Más info a nuestro WhatsApp: +54 9 1167630247""",
        estado="Borrador",
        autor_email="aaaa@gmail.com"
    )

    content3 = content.create_content(
        titulo="Día del Psicólogo y su Rol en TACAs",
        copete="Exploramos el rol del Psicólogo en un Centro de TACAs en Argentina",
        contenido="""Hoy se celebra en Argentina el Día del Psicólog@.
        ¿Cuál es el rol del Psicólogo en un Centro de TACAs?
        El Psicólogo que trabaja en un Centro de TACAs forma parte de un equipo interdisciplinario y desempeña un importante papel en la planificación, implementación y evaluación de las TACAs, propiciando una intervención integral para las diferentes personas con las que trabaja.
        La forma en que nos vinculamos con los caballos, muchas veces es el reflejo de cómo nos vinculamos con otros y pone de relieve cómo nos vemos, cómo nos sentimos. Partiendo de esto, el Psicólogo trabaja para estimular una constitución psíquica saludable, que dé lugar a nuevas formas e imágenes que permitan mejorar la autoestima y favorezcan cada vez mayor independencia y autonomía.
        A través de esta terapia complementaria, el Psicólogo diseña intervenciones para estimular diferentes áreas del desarrollo, y a su vez, ayuda a las personas a desarrollar nuevas formas de pensar, sentir y relacionarse consigo mismos y con los demás.
        Saludamos a tod@s aquell@s Psicólog@s que trabajan y han trabajado en CEDICA 💛 que tengan un feliz día!!""",
        estado="Archivado",
        fecha_publicacion="2021-10-13",
        autor_email="generalLee@gmail.com"
    )

    content4 = content.create_content(
        titulo="Abordaje de la Encefalopatía Crónica No Evolutiva (Parálisis Cerebral) en TACAs",
        copete="Exploramos cómo las Terapias Asistidas con Caballos (TACAs) ayudan en la intervención de la Parálisis Cerebral.",
        contenido="""¿Cómo abordamos la Encefalopatía Crónica No Evolutiva (también conocida como Parálisis Cerebral) desde las TACAs?
        🐎 El Patrón de Locomoción Tridimensional del Caballo permite intervenir en el cuerpo del Jinete/Amazona otorgando mejoras en el Tono Muscular (hipertonía e hipotonía), la Postura y los Movimientos.
        🪷 Permite reducir las asimetrías; alteraciones en la columna vertebral (Lordosis, Cifosis, Escoliosis, en este caso evaluar grado de desviación); promueve mayor capacidad respiratoria y control postural.
        ☀️ Además le brinda un espacio de empoderamiento y autonomía que deja una huella imborrable en la construcción de la PcD y su historia!
        Para más información comunicate con nosotr@s!! 
        📱 +549 1167630247""",
        estado="Publicado",
        fecha_publicacion="2021-11-01",
        autor_email="generalLee@gmail.com"
    )

    content5 = content.create_content(
        titulo="CEDICA celebra 30 años de experiencia en noviembre",
        copete="Acompáñanos en las Jornadas de Actualización en TACAs y el Concurso Ecuestre Integrado para celebrar 30 años de CEDICA.",
        contenido="""CEDICA cumple 30 años de experiencia ✨ y en noviembre nos vamos a encontrar para celebrarlo!!
        Con Jornadas de Actualización Profesional en TACAs y Concurso Ecuestre Integrado 🐴🎖️
        L@s esperamos! 💛🤍💙""",
        estado="Borrador",
        autor_email="aaaa@gmail.com"
    )
    content6 = content.create_content(
        titulo="Un regalo para toda la comunidad de las TACAs 🎁",
        copete="CEDICA celebra 30 años de labor ininterrumpida promoviendo TACAs y el deporte ecuestre adaptado.",
        contenido="""Cumplimos 30 años de labor ininterrumpida realizando Terapias y Actividades Asistidas con Caballos y Deporte Ecuestre Adaptado para Personas con Discapacidad.
        Deseamos que todas las instituciones dedicadas a las TACAs, colegas y familiares sean parte de esta celebración.
        Los esperamos el viernes 15 de noviembre a la Jornada de Actualización Profesional en TACAs de CEDICA, en la Universidad Nacional de La Plata 🇦🇷.
        **Modalidad:** PRESENCIAL en el Aula 10 del Edificio Karakachoff (calle 48 #551) y POR ZOOM para que tod@s puedan estar 🫶🏼.
        La inscripción es gratuita a través del enlace en los comentarios o por WhatsApp al: +5491167630247.""",
        estado="Publicado",
        fecha_publicacion="2022-11-01",
        autor_email="aaaa@gmail.com"
    )

    content7 = content.create_content(
        titulo="INSTRUCTORADO ECUESTRE con modalidad 100% virtual",
        copete="Formación en destrezas y habilidades prácticas para trabajar con caballos dedicados a las TACAs.",
        contenido="""✔️ INSTRUCTORADO ECUESTRE con modalidad 100% virtual, con prácticas presenciales optativas programables.
        Esta capacitación tiene como objetivo desarrollar las destrezas y habilidades prácticas necesarias para seleccionar, entrenar y cuidar caballos específicamente dedicados a las TACAs y DEA.
        La formación capacita a los participantes como responsables ecuestres para desempeñarse como cuidadores, entrenadores o coordinadores del área ecuestre en un Centro de TACAs.
        📱 Para más información, comunicate con nosotros por WhatsApp al: +54 9 1167630247.""",
        estado="Publicado",
        fecha_publicacion="2019-11-01",
        autor_email="generalLee@gmail.com"
    )

    content8 = content.create_content(
        titulo="20 de septiembre | Día Nacional del Caballo 🐴",
        copete="Un homenaje a Mancha y Gato, héroes de la travesía del siglo.",
        contenido="""📌 El 24 de abril de 1925 se inició una de las travesías más memorables: Mancha y Gato, dos caballos criollos guiados por el profesor suizo Aimé F. Tschiffely, recorrieron más de 21 mil kilómetros hasta Nueva York.
        🐎 Conquistaron récords mundiales de distancia y altura, marcando hitos en la historia ecuestre.
        En honor a esta fecha, celebramos el 20 de septiembre como el Día Nacional del Caballo, recordando su importancia histórica, económica y deportiva en Argentina.
        🫶 Gracias a Mancha y Gato por su legado imborrable.""",
        estado="Publicado",
        fecha_publicacion="2020-11-01",
        autor_email="aaaa@gmail.com"
    )

    content9 = content.create_content(
        titulo="El Programa Internacional de Formación Profesional en TACAs",
        copete="Una oportunidad única para profesionales interesados en TACAs y Deporte Ecuestre Adaptado.",
        contenido="""El Programa Internacional de Formación Profesional en Terapias Asistidas con Caballos y Deporte Ecuestre Adaptado de CEDICA te ofrece una oportunidad única para acrecentar tus conocimientos.
        🇨🇴 Contaremos con Elmer Cifuentes Castro, fisioterapeuta e instructor ecuestre de renombre en Latinoamérica, especializado en neurodesarrollo, TACAs y deporte adaptado.
        Para más información, envíanos un WhatsApp al: +5491167630247.
        🌞 Saludos cordiales desde La Plata, Argentina!""",
        estado="Publicado",
        fecha_publicacion="2018-11-01",
        autor_email="generalLee@gmail.com"
    )

    content10 = content.create_content(
        titulo="Clase especial con Giancarlo Garcia Cacción",
        copete="Explorando el potencial humano a través de proyectos creativos.",
        contenido="""Esta semana tenemos una clase especial con Giancarlo Garcia Cacción! 🇪🇨
        Psicólogo educativo y clínico, con un enfoque en trastornos del desarrollo infantil y autismo.
        Actualmente dirige Colmena, una organización enfocada en maximizar el rendimiento juvenil a través de proyectos creativos.
        📱 Para más información, comunicate con nosotros por WhatsApp al: +54 9 1167630247.
        🇦🇷 Saludos desde La Plata, Argentina.""",
        estado="Publicado",
        fecha_publicacion="2017-11-01",
        autor_email="aaaa@gmail.com"
    )
