-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 20-09-2025 a las 01:53:17
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `horizonte_del_saber_2`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_DeleteAsignatura` (IN `p_id_asignatura` INT)   BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Verificar si la asignatura existe
    SELECT COUNT(*) INTO v_count FROM asignaturas WHERE id_asignaturas = p_id_asignatura;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La asignatura no existe';
    END IF;

    -- Verificar relaciones
    SELECT COUNT(*) INTO v_count FROM calificaciones WHERE id_asignaturas = p_id_asignatura;
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede eliminar: la asignatura tiene calificaciones asociadas';
    END IF;

    -- Eliminar relaciones
    DELETE FROM estudiantes_asignaturas WHERE id_asignaturas = p_id_asignatura;
    DELETE FROM asignaturas WHERE id_asignaturas = p_id_asignatura;

    COMMIT;

    SELECT 'Asignatura eliminada correctamente' AS Message;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_DeleteEstudiante` (IN `p_id_estudiante` INT)   BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Verificar si el estudiante existe
    SELECT COUNT(*) INTO v_count FROM estudiantes WHERE Id_estudiantes = p_id_estudiante;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El estudiante no existe';
    END IF;

    -- Eliminar referencias en tablas relacionadas
    DELETE FROM estudiantes_actividades_extracurriculares WHERE dni_estudiante = (SELECT dni FROM estudiantes WHERE Id_estudiantes = p_id_estudiante);
    DELETE FROM estudiantes_asignaturas WHERE dni_estudiante = (SELECT dni FROM estudiantes WHERE Id_estudiantes = p_id_estudiante);
    DELETE FROM estudiantes_cursos WHERE dni_estudiante = (SELECT dni FROM estudiantes WHERE Id_estudiantes = p_id_estudiante);
    DELETE FROM calificaciones WHERE dni_estudiante = (SELECT dni FROM estudiantes WHERE Id_estudiantes = p_id_estudiante);
    DELETE FROM biblioteca WHERE dni_estudiantes = (SELECT dni FROM estudiantes WHERE Id_estudiantes = p_id_estudiante);
    DELETE FROM prestamos WHERE dni_estudiantes = (SELECT dni FROM estudiantes WHERE Id_estudiantes = p_id_estudiante);

    DELETE FROM estudiantes WHERE Id_estudiantes = p_id_estudiante;

    COMMIT;

    SELECT 'Estudiante eliminado correctamente' AS Message;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_DeleteProfesor` (IN `p_id_profesor` INT)   BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Verificar si el profesor existe
    SELECT COUNT(*) INTO v_count FROM profesores WHERE id_profesores = p_id_profesor;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El profesor no existe';
    END IF;

    -- Verificar si tiene cursos asignados
    SELECT COUNT(*) INTO v_count FROM cursos WHERE id_profesores = p_id_profesor;
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No se puede eliminar: el profesor tiene cursos asignados';
    END IF;

    DELETE FROM profesores WHERE id_profesores = p_id_profesor;

    COMMIT;

    SELECT 'Profesor eliminado correctamente' AS Message;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetAllAsignaturas` ()   BEGIN
    SELECT a.*, c.periodo_academico, p.carrera_perteneciente
    FROM asignaturas a
    LEFT JOIN cursos c ON a.id_cursos = c.id_cursos
    LEFT JOIN plan_estudio p ON a.id_plan_estudio = p.id_plan_estudio
    ORDER BY a.nombre;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetAllEstudiantes` ()   BEGIN
    SELECT * FROM estudiantes ORDER BY Apellido, Nombre;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetAllProfesores` ()   BEGIN
    SELECT * FROM profesores ORDER BY apellido, nombre;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetAsignatura` (IN `p_id_asignatura` INT)   BEGIN
    SELECT a.*, c.periodo_academico, p.carrera_perteneciente
    FROM asignaturas a
    LEFT JOIN cursos c ON a.id_cursos = c.id_cursos
    LEFT JOIN plan_estudio p ON a.id_plan_estudio = p.id_plan_estudio
    WHERE a.id_asignaturas = p_id_asignatura;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetCalificacionesPorEstudiante` (IN `p_dni_estudiante` VARCHAR(20))   BEGIN
    SELECT c.*, a.nombre AS asignatura, e.Nombre, e.Apellido
    FROM calificaciones c
    JOIN asignaturas a ON c.id_asignaturas = a.id_asignaturas
    JOIN estudiantes e ON c.dni_estudiante = e.dni
    WHERE c.dni_estudiante = p_dni_estudiante
    ORDER BY c.fecha DESC;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetCursosDisponibles` ()   BEGIN
    SELECT c.id_cursos, CONCAT('Período ', c.periodo_academico, ' - ', c.horarios) AS descripcion
    FROM cursos c
    ORDER BY c.periodo_academico, c.horarios;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetEstadisticasGenerales` ()   BEGIN
    SELECT
        (SELECT COUNT(*) FROM estudiantes) AS total_estudiantes,
        (SELECT COUNT(*) FROM profesores) AS total_profesores,
        (SELECT COUNT(*) FROM asignaturas) AS total_asignaturas,
        (SELECT COUNT(*) FROM biblioteca) AS total_libros,
        (SELECT COUNT(*) FROM cursos) AS total_cursos;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetEstudiante` (IN `p_id_estudiante` INT)   BEGIN
    SELECT * FROM estudiantes WHERE Id_estudiantes = p_id_estudiante;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetPlanesEstudio` ()   BEGIN
    SELECT id_plan_estudio, CONCAT(carrera_perteneciente, ' (', creditos_totales, ' créditos)') AS descripcion
    FROM plan_estudio
    ORDER BY carrera_perteneciente;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetProfesor` (IN `p_id_profesor` INT)   BEGIN
    SELECT * FROM profesores WHERE id_profesores = p_id_profesor;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_InsertAsignatura` (IN `p_cod_asignatura` INT, IN `p_nombre` VARCHAR(50), IN `p_area_crecimiento` VARCHAR(100), IN `p_horas_teoricas` INT, IN `p_horas_practicas` INT, IN `p_creditos_academicos` INT, IN `p_requisitos_previos` TEXT, IN `p_objetivos_generales` TEXT, IN `p_objetivos_especificos` TEXT, IN `p_bibliografica_recomendada` TEXT, IN `p_periodo` VARCHAR(50), IN `p_id_cursos` INT, IN `p_id_plan_estudio` INT)   BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Verificar que existan las referencias
    IF NOT EXISTS (SELECT 1 FROM cursos WHERE id_cursos = p_id_cursos) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El curso especificado no existe';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM plan_estudio WHERE id_plan_estudio = p_id_plan_estudio) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El plan de estudio especificado no existe';
    END IF;

    INSERT INTO asignaturas (
        cod_asignatura, nombre, area_crecimiento, horas_teoricas, horas_practicas,
        creditos_academicos, requisitos_previos, objetivos_generales, objetivos_especificos,
        bibliografica_recomendada, periodo, id_cursos, id_plan_estudio
    )
    VALUES (
        p_cod_asignatura, p_nombre, p_area_crecimiento, p_horas_teoricas, p_horas_practicas,
        p_creditos_academicos, p_requisitos_previos, p_objetivos_generales, p_objetivos_especificos,
        p_bibliografica_recomendada, p_periodo, p_id_cursos, p_id_plan_estudio
    );

    COMMIT;

    SELECT LAST_INSERT_ID() AS id_asignatura, 'Asignatura insertada correctamente' AS Message;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_InsertCalificacion` (IN `p_tipo_evaluacion` ENUM('parcial','final','trabajo','proyecto'), IN `p_fecha` DATE, IN `p_valor_numerico` DECIMAL(10,2), IN `p_porcentaje_total` DECIMAL(5,2), IN `p_observaciones` TEXT, IN `p_dni_estudiante` VARCHAR(20), IN `p_id_cursos` INT, IN `p_id_asignaturas` INT)   BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Verificar referencias
    IF NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = p_dni_estudiante) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El estudiante especificado no existe';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM cursos WHERE id_cursos = p_id_cursos) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El curso especificado no existe';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM asignaturas WHERE id_asignaturas = p_id_asignaturas) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La asignatura especificada no existe';
    END IF;

    INSERT INTO calificaciones (
        tipo_evaluacion, fecha, valor_numerico, porcentaje_total,
        observaciones, dni_estudiante, id_cursos, id_asignaturas
    )
    VALUES (
        p_tipo_evaluacion, p_fecha, p_valor_numerico, p_porcentaje_total,
        p_observaciones, p_dni_estudiante, p_id_cursos, p_id_asignaturas
    );

    COMMIT;

    SELECT LAST_INSERT_ID() AS id_calificacion, 'Calificación insertada correctamente' AS Message;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_InsertEstudiante` (IN `p_matricula` BIGINT, IN `p_nombre` VARCHAR(100), IN `p_apellido` VARCHAR(100), IN `p_dni` VARCHAR(20), IN `p_fecha_nacimiento` DATE, IN `p_direccion` VARCHAR(255), IN `p_telefono` VARCHAR(15), IN `p_correo_electronico` VARCHAR(100), IN `p_nombre_acudiente` VARCHAR(50), IN `p_contacto_emergencia` VARCHAR(50), IN `p_fecha_ingreso` DATE, IN `p_periodo` VARCHAR(50))   BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Verificar que no exista el DNI
    IF EXISTS (SELECT 1 FROM estudiantes WHERE dni = p_dni) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ya existe un estudiante con ese DNI';
    END IF;

    INSERT INTO estudiantes (
        matricula, Nombre, Apellido, dni, Fecha_Nacimiento, Direccion,
        Telefono, Correo_Electronico, Nombre_Acudiente, Contacto_Emergencia,
        Fecha_Ingreso, periodo
    )
    VALUES (
        p_matricula, p_nombre, p_apellido, p_dni, p_fecha_nacimiento, p_direccion,
        p_telefono, p_correo_electronico, p_nombre_acudiente, p_contacto_emergencia,
        p_fecha_ingreso, p_periodo
    );

    COMMIT;

    SELECT LAST_INSERT_ID() AS Id_estudiante, 'Estudiante insertado correctamente' AS Message;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_InsertMaterialBibliografico` (IN `p_cod_material_bibliografico` INT, IN `p_titulo` VARCHAR(255), IN `p_actores` VARCHAR(255), IN `p_editorial` VARCHAR(255), IN `p_ano_publicacion` YEAR, IN `p_edicion` VARCHAR(50), IN `p_isbn` VARCHAR(20), IN `p_categoria_tematica` VARCHAR(100), IN `p_formato` ENUM('Físico','Digital','Audiovisual'), IN `p_ubicacion_fisica` VARCHAR(255), IN `p_cantidad_ejemplares_disponible` INT, IN `p_dni_estudiantes` VARCHAR(20))   BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Verificar que existe el estudiante
    IF NOT EXISTS (SELECT 1 FROM estudiantes WHERE dni = p_dni_estudiantes) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El estudiante especificado no existe';
    END IF;

    INSERT INTO biblioteca (
        cod_material_bibliografico, titulo, actores, editorial, ano_publicacion,
        edicion, isbn, categoria_tematica, formato, ubicacion_fisica,
        cantidad_ejemplares_disponible, dni_estudiantes
    )
    VALUES (
        p_cod_material_bibliografico, p_titulo, p_actores, p_editorial, p_ano_publicacion,
        p_edicion, p_isbn, p_categoria_tematica, p_formato, p_ubicacion_fisica,
        p_cantidad_ejemplares_disponible, p_dni_estudiantes
    );

    COMMIT;

    SELECT LAST_INSERT_ID() AS id_biblioteca, 'Material bibliográfico insertado correctamente' AS Message;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_InsertProfesor` (IN `p_cod_empleado` INT, IN `p_nombre` VARCHAR(50), IN `p_apellido` VARCHAR(100), IN `p_dni` VARCHAR(20), IN `p_fecha_nacimiento` DATE, IN `p_direccion` VARCHAR(255), IN `p_telefono` VARCHAR(15), IN `p_correo_institucional` VARCHAR(100), IN `p_nivel_formacion_academica` VARCHAR(50), IN `p_especialidad` VARCHAR(100), IN `p_anos_experiencia` INT, IN `p_fecha_contratacion` DATE, IN `p_tipo_contrato` ENUM('tiempo completo','medio tiempo','por horas'), IN `p_departamento` VARCHAR(100))   BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Verificar que no existan el código de empleado ni el DNI
    IF EXISTS (SELECT 1 FROM profesores WHERE cod_empleado = p_cod_empleado) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ya existe un profesor con ese código de empleado';
    END IF;

    IF EXISTS (SELECT 1 FROM profesores WHERE dni = p_dni) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ya existe un profesor con ese DNI';
    END IF;

    INSERT INTO profesores (
        cod_empleado, nombre, apellido, dni, fecha_nacimiento, direccion,
        telefono, correo_institucional, nivel_formacion_academica, especialidad,
        anos_experiencia, fecha_contratacion, tipo_contrato, departamento
    )
    VALUES (
        p_cod_empleado, p_nombre, p_apellido, p_dni, p_fecha_nacimiento, p_direccion,
        p_telefono, p_correo_institucional, p_nivel_formacion_academica, p_especialidad,
        p_anos_experiencia, p_fecha_contratacion, p_tipo_contrato, p_departamento
    );

    COMMIT;

    SELECT LAST_INSERT_ID() AS id_profesor, 'Profesor insertado correctamente' AS Message;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_SearchBiblioteca` (IN `p_search_term` VARCHAR(255))   BEGIN
    SELECT * FROM biblioteca
    WHERE titulo LIKE CONCAT('%', p_search_term, '%')
       OR actores LIKE CONCAT('%', p_search_term, '%')
       OR categoria_tematica LIKE CONCAT('%', p_search_term, '%')
       OR isbn LIKE CONCAT('%', p_search_term, '%')
    ORDER BY titulo;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_SearchEstudiantes` (IN `p_search_term` VARCHAR(100))   BEGIN
    SELECT * FROM estudiantes
    WHERE Nombre LIKE CONCAT('%', p_search_term, '%')
       OR Apellido LIKE CONCAT('%', p_search_term, '%')
       OR dni LIKE CONCAT('%', p_search_term, '%')
       OR CAST(matricula AS CHAR) LIKE CONCAT('%', p_search_term, '%')
    ORDER BY Apellido, Nombre;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_SearchProfesores` (IN `p_search_term` VARCHAR(100))   BEGIN
    SELECT * FROM profesores
    WHERE nombre LIKE CONCAT('%', p_search_term, '%')
       OR apellido LIKE CONCAT('%', p_search_term, '%')
       OR dni LIKE CONCAT('%', p_search_term, '%')
       OR especialidad LIKE CONCAT('%', p_search_term, '%')
       OR departamento LIKE CONCAT('%', p_search_term, '%')
    ORDER BY apellido, nombre;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_UpdateAsignatura` (IN `p_id_asignatura` INT, IN `p_cod_asignatura` INT, IN `p_nombre` VARCHAR(50), IN `p_area_crecimiento` VARCHAR(100), IN `p_horas_teoricas` INT, IN `p_horas_practicas` INT, IN `p_creditos_academicos` INT, IN `p_requisitos_previos` TEXT, IN `p_objetivos_generales` TEXT, IN `p_objetivos_especificos` TEXT, IN `p_bibliografica_recomendada` TEXT, IN `p_periodo` VARCHAR(50), IN `p_id_cursos` INT, IN `p_id_plan_estudio` INT)   BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Verificar si la asignatura existe
    SELECT COUNT(*) INTO v_count FROM asignaturas WHERE id_asignaturas = p_id_asignatura;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'La asignatura no existe';
    END IF;

    -- Verificar referencias
    IF NOT EXISTS (SELECT 1 FROM cursos WHERE id_cursos = p_id_cursos) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El curso especificado no existe';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM plan_estudio WHERE id_plan_estudio = p_id_plan_estudio) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El plan de estudio especificado no existe';
    END IF;

    UPDATE asignaturas
    SET cod_asignatura = p_cod_asignatura,
        nombre = p_nombre,
        area_crecimiento = p_area_crecimiento,
        horas_teoricas = p_horas_teoricas,
        horas_practicas = p_horas_practicas,
        creditos_academicos = p_creditos_academicos,
        requisitos_previos = p_requisitos_previos,
        objetivos_generales = p_objetivos_generales,
        objetivos_especificos = p_objetivos_especificos,
        bibliografica_recomendada = p_bibliografica_recomendada,
        periodo = p_periodo,
        id_cursos = p_id_cursos,
        id_plan_estudio = p_id_plan_estudio
    WHERE id_asignaturas = p_id_asignatura;

    COMMIT;

    SELECT 'Asignatura actualizada correctamente' AS Message;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_UpdateEstudiante` (IN `p_id_estudiante` INT, IN `p_matricula` BIGINT, IN `p_nombre` VARCHAR(100), IN `p_apellido` VARCHAR(100), IN `p_dni` VARCHAR(20), IN `p_fecha_nacimiento` DATE, IN `p_direccion` VARCHAR(255), IN `p_telefono` VARCHAR(15), IN `p_correo_electronico` VARCHAR(100), IN `p_nombre_acudiente` VARCHAR(50), IN `p_contacto_emergencia` VARCHAR(50), IN `p_periodo` VARCHAR(50))   BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Verificar si el estudiante existe
    SELECT COUNT(*) INTO v_count FROM estudiantes WHERE Id_estudiantes = p_id_estudiante;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El estudiante no existe';
    END IF;

    -- Verificar que no exista otro estudiante con el mismo DNI
    SELECT COUNT(*) INTO v_count FROM estudiantes WHERE dni = p_dni AND Id_estudiantes != p_id_estudiante;
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ya existe otro estudiante con ese DNI';
    END IF;

    UPDATE estudiantes
    SET matricula = p_matricula,
        Nombre = p_nombre,
        Apellido = p_apellido,
        dni = p_dni,
        Fecha_Nacimiento = p_fecha_nacimiento,
        Direccion = p_direccion,
        Telefono = p_telefono,
        Correo_Electronico = p_correo_electronico,
        Nombre_Acudiente = p_nombre_acudiente,
        Contacto_Emergencia = p_contacto_emergencia,
        periodo = p_periodo
    WHERE Id_estudiantes = p_id_estudiante;

    COMMIT;

    SELECT 'Estudiante actualizado correctamente' AS Message;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_UpdateProfesor` (IN `p_id_profesor` INT, IN `p_cod_empleado` INT, IN `p_nombre` VARCHAR(50), IN `p_apellido` VARCHAR(100), IN `p_dni` VARCHAR(20), IN `p_fecha_nacimiento` DATE, IN `p_direccion` VARCHAR(255), IN `p_telefono` VARCHAR(15), IN `p_correo_institucional` VARCHAR(100), IN `p_nivel_formacion_academica` VARCHAR(50), IN `p_especialidad` VARCHAR(100), IN `p_anos_experiencia` INT, IN `p_fecha_contratacion` DATE, IN `p_tipo_contrato` ENUM('tiempo completo','medio tiempo','por horas'), IN `p_departamento` VARCHAR(100))   BEGIN
    DECLARE v_count INT DEFAULT 0;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    -- Verificar si el profesor existe
    SELECT COUNT(*) INTO v_count FROM profesores WHERE id_profesores = p_id_profesor;
    IF v_count = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'El profesor no existe';
    END IF;

    -- Verificar unicidad de código de empleado y DNI
    SELECT COUNT(*) INTO v_count FROM profesores WHERE cod_empleado = p_cod_empleado AND id_profesores != p_id_profesor;
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ya existe otro profesor con ese código de empleado';
    END IF;

    SELECT COUNT(*) INTO v_count FROM profesores WHERE dni = p_dni AND id_profesores != p_id_profesor;
    IF v_count > 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ya existe otro profesor con ese DNI';
    END IF;

    UPDATE profesores
    SET cod_empleado = p_cod_empleado,
        nombre = p_nombre,
        apellido = p_apellido,
        dni = p_dni,
        fecha_nacimiento = p_fecha_nacimiento,
        direccion = p_direccion,
        telefono = p_telefono,
        correo_institucional = p_correo_institucional,
        nivel_formacion_academica = p_nivel_formacion_academica,
        especialidad = p_especialidad,
        anos_experiencia = p_anos_experiencia,
        fecha_contratacion = p_fecha_contratacion,
        tipo_contrato = p_tipo_contrato,
        departamento = p_departamento
    WHERE id_profesores = p_id_profesor;

    COMMIT;

    SELECT 'Profesor actualizado correctamente' AS Message;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actividades_extracurriculares`
--

CREATE TABLE `actividades_extracurriculares` (
  `id_actividades_extracurriculares` int(11) NOT NULL,
  `cod_actividad` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `id_profesores` int(11) NOT NULL,
  `horario` varchar(100) NOT NULL,
  `lugar` varchar(255) NOT NULL,
  `cupo` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `actividades_extracurriculares`
--

INSERT INTO `actividades_extracurriculares` (`id_actividades_extracurriculares`, `cod_actividad`, `nombre`, `tipo`, `descripcion`, `id_profesores`, `horario`, `lugar`, `cupo`) VALUES
(1, 501, 'Club de Lectura', 'Cultural', 'Lectura y análisis de obras literarias', 1, 'Martes 4-6PM', 'Aula 101', 20),
(2, 502, 'Taller de Fotografía', 'Artístico', 'Aprendizaje de técnicas de fotografía', 2, 'Jueves 2-4PM', 'Laboratorio Multimedia', 15),
(3, 503, 'Equipo de Fútbol', 'Deportivo', 'Entrenamiento y preparación para torneos', 3, 'Lunes y Miércoles 5-7PM', 'Campo Deportivo', 25),
(4, 504, 'Orquesta Universitaria', 'Cultural', 'Práctica y presentación de música clásica', 4, 'Viernes 6-8PM', 'Auditorio Principal', 30),
(5, 505, 'Taller de Cocina', 'Recreativo', 'Aprendizaje de recetas y técnicas culinarias', 5, 'Sábado 10AM-12PM', 'Cocina Taller', 10),
(6, 506, 'Concurso de Debate', 'Académico', 'Preparación para competiciones de debate', 6, 'Miércoles 3-5PM', 'Sala de Conferencias', 20),
(7, 507, 'Grupo de Teatro', 'Cultural', 'Ensayos y presentaciones de obras teatrales', 7, 'Lunes y Jueves 4-6PM', 'Teatro Universitario', 25),
(8, 508, 'Taller de Dibujo', 'Artístico', 'Clases prácticas de técnicas de dibujo', 8, 'Martes y Jueves 2-4PM', 'Aula de Arte', 15),
(9, 509, 'Clases de Yoga', 'Recreativo', 'Práctica de yoga para relajación y bienestar', 9, 'Martes y Viernes 7-8AM', 'Gimnasio', 20),
(10, 510, 'Voluntariado Social', 'Comunitario', 'Organización de eventos para apoyo comunitario', 10, 'Sábado 9AM-12PM', 'Centro Comunitario', 50);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asignaturas`
--

CREATE TABLE `asignaturas` (
  `id_asignaturas` int(11) NOT NULL,
  `cod_asignatura` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `area_crecimiento` varchar(100) NOT NULL,
  `horas_teoricas` int(11) NOT NULL,
  `horas_practicas` int(11) NOT NULL,
  `creditos_academicos` int(11) NOT NULL,
  `requisitos_previos` text DEFAULT NULL,
  `objetivos_generales` text DEFAULT NULL,
  `objetivos_especificos` text DEFAULT NULL,
  `bibliografica_recomendada` text DEFAULT NULL,
  `periodo` varchar(50) NOT NULL,
  `id_cursos` int(11) NOT NULL,
  `id_plan_estudio` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `asignaturas`
--

INSERT INTO `asignaturas` (`id_asignaturas`, `cod_asignatura`, `nombre`, `area_crecimiento`, `horas_teoricas`, `horas_practicas`, `creditos_academicos`, `requisitos_previos`, `objetivos_generales`, `objetivos_especificos`, `bibliografica_recomendada`, `periodo`, `id_cursos`, `id_plan_estudio`) VALUES
(1, 301, 'Programación Avanzada', 'Desarrollo Tecnológico', 30, 20, 5, 'Conocimientos básicos de programación', 'Desarrollar habilidades en lenguajes modernos', 'Implementar sistemas complejos', 'Manual de Python, Guía de Java', '1° año', 1, 1),
(2, 302, 'Biología Molecular', 'Ciencias Naturales', 25, 35, 6, 'Biología General', 'Entender los procesos moleculares en organismos vivos', 'Estudiar técnicas de laboratorio molecular', 'Biología Molecular por Alberts', '2° año', 2, 2),
(3, 303, 'software avanzado', 'Humanidades', 20, 15, 3, 'Introducción a la Filosofía', 'Analizar el pensamiento filosófico contemporáneo', 'Comparar diferentes corrientes modernas', 'Historia de la Filosofía por Russell', '3° año', 3, 3),
(4, 304, 'Cálculo Integral', 'Matemáticas', 40, 10, 4, 'Cálculo Diferencial', 'Aplicar el cálculo en problemas del mundo real', 'Solución de integrales complejas', 'Cálculo por Stewart', '4° año', 4, 4),
(5, 305, 'Química Orgánica', 'Ciencias Naturales', 35, 25, 5, 'Química General', 'Estudiar compuestos orgánicos y sus reacciones', 'Prácticas experimentales en química orgánica', 'Química Orgánica por McMurry', '5° año', 5, 5),
(6, 306, 'Historia Universal', 'Humanidades', 30, 15, 4, 'Historia Antigua', 'Explorar los eventos clave de la historia mundial', 'Analizar documentos históricos', 'Atlas Histórico Mundial', '6° año', 6, 6),
(7, 307, 'Dinámica de Sistemas', 'Ingeniería Mecánica', 40, 20, 6, 'Fundamentos de Mecánica', 'Entender el comportamiento dinámico de sistemas físicos', 'Simulación de sistemas mecánicos', 'Dinámica de Sistemas por Ogata', '7° año', 7, 7),
(8, 308, 'Arte Contemporáneo', 'Artes Visuales', 20, 30, 5, 'Historia del Arte', 'Explorar movimientos artísticos actuales', 'Creación de obras contemporáneas', 'Arte Contemporáneo por González', '8° año', 8, 8),
(9, 309, 'Gestión Empresarial', 'Negocios', 30, 20, 5, 'Introducción a la Administración', 'Desarrollar habilidades gerenciales', 'Análisis de casos empresariales', 'Gestión Empresarial por Kotler', '9° año', 9, 9),
(10, 310, 'Lingüística Aplicada', 'Humanidades', 25, 20, 4, 'Introducción a la Lingüística', 'Aplicar principios lingüísticos a problemas reales', 'Estudio de variaciones lingüísticas', 'Lingüística Aplicada por Crystal', '10° año', 10, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `aulas`
--

CREATE TABLE `aulas` (
  `id_aulas` int(11) NOT NULL,
  `numero_identificador` varchar(20) NOT NULL,
  `edificio` varchar(50) NOT NULL,
  `piso` int(11) NOT NULL,
  `capacidad_estudiantes` int(11) NOT NULL,
  `tipo` enum('Teórica','Laboratorio','Taller') NOT NULL,
  `equipamiento_disponible` text DEFAULT NULL,
  `estado_actual` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `aulas`
--

INSERT INTO `aulas` (`id_aulas`, `numero_identificador`, `edificio`, `piso`, `capacidad_estudiantes`, `tipo`, `equipamiento_disponible`, `estado_actual`) VALUES
(1, '101', 'Edificio Central', 1, 30, 'Laboratorio', 'Computadoras, proyector', 'Disponible'),
(2, '102', 'Edificio Ciencias', 2, 50, 'Teórica', 'Pizarra, sillas, mesa de profesor', 'Disponible'),
(3, '103', 'Edificio Ingeniería', 3, 40, 'Laboratorio', 'Computadoras, kits de robótica', 'En Mantenimiento'),
(4, '104', 'Edificio Humanidades', 1, 25, 'Teórica', 'Pizarra interactiva, sillas ergonómicas', 'Disponible'),
(5, '105', 'Edificio Matemáticas', 2, 20, 'Taller', 'Pizarra, proyectores', 'Reservada'),
(6, '106', 'Edificio Ciencias', 3, 35, 'Laboratorio', 'Microscopios, cámaras digitales', 'Disponible'),
(7, '107', 'Edificio Central', 1, 50, 'Laboratorio', 'Proyector, sonido integrado', 'Disponible'),
(8, '108', 'Edificio Idiomas', 2, 15, 'Taller', 'Computadoras, auriculares', 'Disponible'),
(9, '198', 'Edificio Ingeniería', 4, 60, 'Teórica', 'Pizarra, equipo audiovisual', 'En Mantenimiento'),
(10, '110', 'Edificio Ciencias', 3, 25, 'Teórica', 'Mesas grupales, pizarras blancas', 'Reservada');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `biblioteca`
--

CREATE TABLE `biblioteca` (
  `id_biblioteca` int(11) NOT NULL,
  `cod_material_bibliografico` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `actores` varchar(255) DEFAULT NULL,
  `editorial` varchar(255) DEFAULT NULL,
  `ano_publicacion` year(4) NOT NULL,
  `edicion` varchar(50) DEFAULT NULL,
  `isbn` varchar(20) NOT NULL,
  `categoria_tematica` varchar(100) NOT NULL,
  `formato` enum('Físico','Digital','Audiovisual') NOT NULL,
  `ubicacion_fisica` varchar(255) DEFAULT NULL,
  `cantidad_ejemplares_disponible` int(11) NOT NULL,
  `dni_estudiantes` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `biblioteca`
--

INSERT INTO `biblioteca` (`id_biblioteca`, `cod_material_bibliografico`, `titulo`, `actores`, `editorial`, `ano_publicacion`, `edicion`, `isbn`, `categoria_tematica`, `formato`, `ubicacion_fisica`, `cantidad_ejemplares_disponible`, `dni_estudiantes`) VALUES
(1, 1001, 'Introducción a la Programación', 'John Doe', NULL, '2020', 'Primera', '978-1234567890', 'Tecnología', 'Físico', 'Estante A1', 5, '3467829154'),
(2, 1002, 'Química General', 'Jane Smith', NULL, '2018', 'Segunda', '978-0987654321', 'Ciencias', 'Digital', 'Estante B2', 10, '3467829155'),
(3, 1003, 'Historia Universal Contemporánea', 'George Johnson', NULL, '2015', 'Tercera', '978-1122334455', 'Historia', 'Físico', 'Estante C4', 4, '3467829156'),
(4, 1004, 'Arte Moderno y Contemporáneo', 'Ana Pérez', NULL, '2019', 'Primera', '978-2233445566', 'Arte', 'Audiovisual', 'Sala Audiovisual', 2, '3467829157'),
(5, 1005, 'Física Cuántica', 'Albert Einstein', NULL, '2021', 'Cuarta', '978-3344556677', 'Ciencias', 'Físico', 'Estante B3', 6, '3467829158'),
(6, 1006, 'Marketing Digital', 'Sarah Brown', NULL, '2022', 'Primera', '978-4455667788', 'Negocios', 'Digital', 'Estante D1', 8, '3467829159'),
(7, 1007, 'Teoría de la Relatividad', 'Albert Einstein', NULL, '2007', 'Décima', '978-5566778899', 'Ciencias', 'Físico', 'Estante A5', 3, '3467829160'),
(8, 1008, 'Lingüística Aplicada', 'Noah Davis', NULL, '2016', 'Segunda', '978-6677889900', 'Humanidades', 'Físico', 'Estante D2', 7, '3467829161'),
(9, 1009, 'Cálculo Diferencial e Integral', 'Isaac Newton', NULL, '2014', 'Primera', '978-7788990011', 'Matemáticas', 'Físico', 'Estante C1', 5, '3467829162'),
(10, 1010, 'Biología Molecular', 'James Watson', NULL, '2023', 'Primera', '978-8899001122', 'Ciencias', 'Audiovisual', 'Laboratorio 101', 3, '3467829163');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `calificaciones`
--

CREATE TABLE `calificaciones` (
  `id_calificaciones` int(11) NOT NULL,
  `tipo_evaluacion` enum('parcial','final','trabajo','proyecto') NOT NULL,
  `fecha` date NOT NULL,
  `valor_numerico` decimal(10,2) DEFAULT NULL,
  `porcentaje_total` decimal(5,2) DEFAULT NULL,
  `observaciones` text DEFAULT NULL,
  `dni_estudiante` varchar(20) NOT NULL,
  `id_cursos` int(11) NOT NULL,
  `id_asignaturas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `calificaciones`
--

INSERT INTO `calificaciones` (`id_calificaciones`, `tipo_evaluacion`, `fecha`, `valor_numerico`, `porcentaje_total`, `observaciones`, `dni_estudiante`, `id_cursos`, `id_asignaturas`) VALUES
(1, 'parcial', '2025-03-01', 4.50, 20.00, 'Buen desempeño en el parcial.', '3467829154', 1, 1),
(2, 'final', '2025-03-10', 3.80, 50.00, 'Mejorable en algunos aspectos.', '3467829155', 2, 2),
(3, 'trabajo', '2025-02-25', 5.00, 10.00, 'Excelente trabajo entregado.', '3467829156', 3, 3),
(4, 'proyecto', '2025-03-15', 4.00, 20.00, 'Buena presentación del proyecto.', '3467829157', 4, 4),
(5, 'parcial', '2025-01-20', 4.20, 30.00, 'Correcto pero algo ajustado.', '3467829158', 5, 5),
(6, 'final', '2025-01-30', 3.50, 40.00, 'Promedio en resultados.', '3467829159', 6, 6),
(7, 'trabajo', '2025-03-05', 4.80, 15.00, 'Entrega impecable.', '3467829160', 7, 7),
(8, 'proyecto', '2025-02-28', 3.90, 25.00, 'Aspectos a mejorar.', '3467829161', 8, 8),
(9, 'parcial', '2025-02-10', 4.00, 20.00, 'Resultados satisfactorios.', '3467829162', 9, 9),
(10, 'final', '2025-03-20', 3.70, 45.00, 'Buena participación en general.', '3467829163', 10, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cursos`
--

CREATE TABLE `cursos` (
  `id_cursos` int(11) NOT NULL,
  `periodo_academico` int(11) NOT NULL,
  `horarios` varchar(50) NOT NULL,
  `cupo_maximo` int(11) NOT NULL,
  `metodologia_evaluacion` text DEFAULT NULL,
  `id_aulas` int(11) NOT NULL,
  `id_profesores` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cursos`
--

INSERT INTO `cursos` (`id_cursos`, `periodo_academico`, `horarios`, `cupo_maximo`, `metodologia_evaluacion`, `id_aulas`, `id_profesores`) VALUES
(1, 2023, 'Lunes 8-10AM', 30, 'Evaluación continua', 1, 1),
(2, 2023, 'Martes 10-12AM', 25, 'Proyectos grupales', 2, 2),
(3, 2023, 'Miércoles 2-4PM', 20, 'Pruebas teóricas', 3, 3),
(4, 2024, 'Jueves 1-3PM', 35, 'Prácticas de campo', 4, 4),
(5, 2024, 'Viernes 9-11AM', 40, 'Exámenes escritos', 5, 5),
(6, 2024, 'Sábado 3-5PM', 50, 'Evaluación por rúbricas', 6, 6),
(7, 2023, 'Lunes 5-7PM', 30, 'Estudio independiente', 7, 7),
(8, 2023, 'Martes 7-9AM', 25, 'Actividades en laboratorio', 8, 8),
(9, 2024, 'Miércoles 4-6PM', 20, 'Participación oral', 9, 9),
(10, 2023, 'Jueves 8-10AM', 35, 'Evaluación continua', 10, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes`
--

CREATE TABLE `estudiantes` (
  `Id_estudiantes` int(11) NOT NULL,
  `matricula` bigint(20) NOT NULL,
  `Nombre` varchar(100) NOT NULL,
  `Apellido` varchar(100) NOT NULL,
  `dni` varchar(20) NOT NULL,
  `Fecha_Nacimiento` date NOT NULL,
  `Direccion` varchar(255) NOT NULL,
  `Telefono` varchar(15) DEFAULT NULL,
  `Correo_Electronico` varchar(100) DEFAULT NULL,
  `Fotografia` blob DEFAULT NULL,
  `Nombre_Acudiente` varchar(50) NOT NULL,
  `Contacto_Emergencia` varchar(50) NOT NULL,
  `Fecha_Ingreso` date NOT NULL,
  `periodo` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiantes`
--

INSERT INTO `estudiantes` (`Id_estudiantes`, `matricula`, `Nombre`, `Apellido`, `dni`, `Fecha_Nacimiento`, `Direccion`, `Telefono`, `Correo_Electronico`, `Fotografia`, `Nombre_Acudiente`, `Contacto_Emergencia`, `Fecha_Ingreso`, `periodo`) VALUES
(1, 8274615932, 'Ernesto', 'Cadavid', '3467829154', '2000-04-12', 'Calle 123, Barrio Los Cedros, Ciudad Sol, Colombia', '3114820975', 'juan.perez@horizontes.edu.co', NULL, 'Ana Mesa', '311-852-7436', '2023-01-13', '1° año'),
(2, 8274615933, 'María', 'González', '3467829155', '2001-06-15', 'Carrera 45, Edificio Las Palmas, Medellín, Colombia', '3105678901', 'maria.gonzalez@horizontedelsaber.edu.co', NULL, 'Carlos González', '320-567-4321', '2023-02-01', '2° año'),
(3, 8274615934, 'Juan', 'López', '3467829156', '1999-09-25', 'Calle 67, Urbanización El Pinar, Bogotá, Colombia', '3139876543', 'juan.lopez@horizontedelsaber.edu.co', NULL, 'Sofía López', '311-987-6543', '2023-01-20', '3° año'),
(4, 8274615935, 'Camila', 'Pérez', '3467829157', '2002-01-30', 'Avenida 12, Barrio San Antonio, Cali, Colombia', '3162345678', 'camila.perez@horizontedelsaber.edu.co', NULL, 'Roberto Pérez', '312-345-6789', '2023-01-25', '4° año'),
(5, 8274615936, 'Diego', 'Ramírez', '3467829158', '1998-11-22', 'Carrera 21, Apartamento Las Flores, Cartagena, Colombia', '3147654321', 'diego.ramirez@horizontedelsaber.edu.co', NULL, 'Patricia Ramírez', '315-765-4321', '2023-03-01', '5° año'),
(6, 8274615937, 'Laura', 'Mejía', '3467829159', '2001-08-14', 'Calle 50, Residencial El Nogal, Manizales, Colombia', '3158745632', 'laura.mejia@horizontedelsaber.edu.co', NULL, 'Andrés Mejía', '317-854-9632', '2023-02-05', '6° año'),
(7, 8274615938, 'Andrés', 'Zuluaga', '3467829160', '1997-05-03', 'Carrera 18, Barrio La Aurora, Armenia, Colombia', '3109674532', 'andres.zuluaga@horizontedelsaber.edu.co', NULL, 'Carolina Zuluaga', '312-784-5632', '2023-03-12', '7° año'),
(8, 8274615939, 'Paola', 'Cardona', '3467829161', '1999-10-28', 'Calle 32, Barrio El Sol, Bucaramanga, Colombia', '3195678234', 'paola.cardona@horizontedelsaber.edu.co', NULL, 'Luis Cardona', '316-973-4521', '2023-01-15', '8° año'),
(9, 8274615940, 'Esteban', 'Martínez', '3467829162', '2003-02-11', 'Avenida 10, Residencias La Paz, Villavicencio, Colombia', '3126549781', 'esteban.martinez@horizontedelsaber.edu.co', NULL, 'Rosa Martínez', '318-652-4175', '2023-01-18', '9° año'),
(10, 8274615941, 'Sofía', 'Velásquez', '3467829163', '2000-12-20', 'Carrera 5, Urbanización Las Lomas, Pereira, Colombia', '3207846591', 'sofia.velasquez@horizontedelsaber.edu.co', NULL, 'Mario Velásquez', '310-845-7963', '2023-02-20', '10° año');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes_actividades_extracurriculares`
--

CREATE TABLE `estudiantes_actividades_extracurriculares` (
  `id_estudiantes_actividades_extracurriculares` int(11) NOT NULL,
  `dni_estudiante` varchar(20) NOT NULL,
  `id_actividades_extracurriculares` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiantes_actividades_extracurriculares`
--

INSERT INTO `estudiantes_actividades_extracurriculares` (`id_estudiantes_actividades_extracurriculares`, `dni_estudiante`, `id_actividades_extracurriculares`) VALUES
(1, '3467829154', 1),
(2, '3467829155', 2),
(3, '3467829156', 3),
(4, '3467829157', 4),
(5, '3467829158', 5),
(6, '3467829159', 6),
(7, '3467829160', 7),
(8, '3467829161', 8),
(9, '3467829162', 9),
(10, '3467829163', 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes_asignaturas`
--

CREATE TABLE `estudiantes_asignaturas` (
  `id_estudiantes_asignaturas` int(11) NOT NULL,
  `dni_estudiante` varchar(20) NOT NULL,
  `id_asignaturas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiantes_asignaturas`
--

INSERT INTO `estudiantes_asignaturas` (`id_estudiantes_asignaturas`, `dni_estudiante`, `id_asignaturas`) VALUES
(1, '3467829154', 1),
(2, '3467829155', 2),
(3, '3467829156', 3),
(4, '3467829157', 4),
(5, '3467829158', 5),
(6, '3467829159', 6),
(7, '3467829160', 7),
(8, '3467829161', 8),
(9, '3467829162', 9),
(10, '3467829163', 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes_cursos`
--

CREATE TABLE `estudiantes_cursos` (
  `id_estudiantes_cursos` int(11) NOT NULL,
  `dni_estudiante` varchar(20) NOT NULL,
  `id_cursos` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiantes_cursos`
--

INSERT INTO `estudiantes_cursos` (`id_estudiantes_cursos`, `dni_estudiante`, `id_cursos`) VALUES
(1, '3467829154', 1),
(2, '3467829155', 2),
(3, '3467829156', 3),
(4, '3467829157', 4),
(5, '3467829158', 5),
(6, '3467829159', 6),
(7, '3467829160', 7),
(8, '3467829161', 8),
(9, '3467829162', 9),
(10, '3467829163', 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `plan_estudio`
--

CREATE TABLE `plan_estudio` (
  `id_plan_estudio` int(11) NOT NULL,
  `cod_plan_estudio` int(11) NOT NULL,
  `carrera_perteneciente` varchar(50) NOT NULL,
  `fecha_aprobacion` date NOT NULL,
  `asignatura_nivel` int(11) NOT NULL,
  `creditos_totales` int(11) NOT NULL,
  `requisitos_graduacion` text DEFAULT NULL,
  `id_cursos` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `plan_estudio`
--

INSERT INTO `plan_estudio` (`id_plan_estudio`, `cod_plan_estudio`, `carrera_perteneciente`, `fecha_aprobacion`, `asignatura_nivel`, `creditos_totales`, `requisitos_graduacion`, `id_cursos`) VALUES
(1, 201, 'Ingeniería de Software', '2022-03-15', 1, 120, 'Proyecto final de desarrollo', 1),
(2, 202, 'Ciencias Biológicas', '2021-06-10', 2, 140, 'Prácticas en laboratorio', 2),
(3, 203, 'Filosofía', '2020-09-20', 3, 100, 'Tesis sobre ética', 3),
(4, 204, 'Matemáticas Aplicadas', '2023-02-01', 1, 130, 'Resolución de problemas avanzados', 4),
(5, 205, 'Química', '2022-08-12', 2, 150, 'Prácticas y análisis químicos', 5),
(6, 206, 'Historia', '2021-11-05', 3, 110, 'Investigación histórica', 6),
(7, 207, 'Ingeniería Mecánica', '2023-01-18', 1, 160, 'Diseño de un prototipo funcional', 7),
(8, 208, 'Artes Visuales', '2020-04-22', 4, 120, 'Exposición artística final', 8),
(9, 209, 'Administración de Empresas', '2021-07-30', 3, 140, 'Prácticas empresariales', 9),
(10, 210, 'Estudios Lingüísticos', '2022-12-10', 2, 125, 'Ensayo lingüístico avanzado', 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `prestamos`
--

CREATE TABLE `prestamos` (
  `id_prestamos` int(11) NOT NULL,
  `cod_prestamos` int(11) NOT NULL,
  `fecha_prestamo` date NOT NULL,
  `fecha_devolucion` date NOT NULL,
  `estado` varchar(50) NOT NULL,
  `multas_aplicadas` decimal(5,2) NOT NULL,
  `id_profesores` int(11) NOT NULL,
  `dni_estudiantes` varchar(20) NOT NULL,
  `id_biblioteca` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `prestamos`
--

INSERT INTO `prestamos` (`id_prestamos`, `cod_prestamos`, `fecha_prestamo`, `fecha_devolucion`, `estado`, `multas_aplicadas`, `id_profesores`, `dni_estudiantes`, `id_biblioteca`) VALUES
(1, 1001, '2023-03-01', '2023-03-15', 'Devuelto', 0.00, 1, '3467829154', 1),
(2, 1002, '2023-03-05', '2023-03-20', 'Pendiente', 50.00, 2, '3467829155', 2),
(3, 1003, '2023-03-10', '2023-03-25', 'Devuelto', 0.00, 3, '3467829156', 3),
(4, 1004, '2023-03-15', '2023-03-30', 'Devuelto', 20.00, 4, '3467829157', 4),
(5, 1005, '2023-03-20', '2023-04-05', 'Pendiente', 0.00, 5, '3467829158', 5),
(6, 1006, '2023-03-25', '2023-04-10', 'Devuelto', 10.00, 6, '3467829159', 6),
(7, 1007, '2023-03-30', '2023-04-15', 'Pendiente', 0.00, 7, '3467829160', 7),
(8, 1008, '2023-04-01', '2023-04-16', 'Devuelto', 30.00, 8, '3467829161', 8),
(9, 1009, '2023-04-05', '2023-04-20', 'Pendiente', 0.00, 9, '3467829162', 9),
(10, 1010, '2023-04-10', '2023-04-25', 'Devuelto', 15.00, 10, '3467829163', 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesores`
--

CREATE TABLE `profesores` (
  `id_profesores` int(11) NOT NULL,
  `cod_empleado` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `dni` varchar(20) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `correo_institucional` varchar(100) NOT NULL,
  `nivel_formacion_academica` varchar(50) NOT NULL,
  `especialidad` varchar(100) DEFAULT NULL,
  `anos_experiencia` int(11) DEFAULT NULL,
  `fecha_contratacion` date NOT NULL,
  `tipo_contrato` enum('tiempo completo','medio tiempo','por horas') NOT NULL,
  `departamento` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `profesores`
--

INSERT INTO `profesores` (`id_profesores`, `cod_empleado`, `nombre`, `apellido`, `dni`, `fecha_nacimiento`, `direccion`, `telefono`, `correo_institucional`, `nivel_formacion_academica`, `especialidad`, `anos_experiencia`, `fecha_contratacion`, `tipo_contrato`, `departamento`) VALUES
(1, 1001, 'Carlos', 'Ramírez', '1234567890', '1980-04-15', 'Calle 10, Medellín, Colombia', '3124567890', 'carlos.ramirez@horizontesdelsaber.edu.co', 'Maestría', 'Matemáticas', 10, '2024-01-02', 'tiempo completo', 'Ciencias Exactas'),
(2, 1002, 'Ana', 'Gómez', '9876543210', '1975-06-25', 'Carrera 45, Bogotá, Colombia', '3109876543', 'ana.gomez@horizontesdelsaber.edu.co', 'Doctorado', 'Ciencias Naturales', 15, '2024-12-02', 'medio tiempo', 'Biología'),
(3, 1003, 'Juan', 'López', '2468101214', '1985-12-05', 'Avenida 20, Cali, Colombia', '3135551234', 'juan.lopez@horizontesdelsaber.edu.co', 'Licenciatura', 'Historia', 8, '2024-10-24', 'por horas', 'Humanidades'),
(4, 1004, 'Marta', 'Velásquez', '1357913579', '1990-03-11', 'Calle 50, Barranquilla, Colombia', '3148901234', 'marta.velasquez@horizontesdelsaber.edu.co', 'Maestría', 'Física', 12, '2024-10-18', 'tiempo completo', 'Física Aplicada'),
(5, 1005, 'Luis', 'Martínez', '5678901234', '1982-07-20', 'Calle 12, Manizales, Colombia', '3156789012', 'luis.martinez@horizontesdelsaber.edu.co', 'Doctorado', 'Ingeniería Electrónica', 20, '2024-10-18', 'medio tiempo', 'Ingeniería'),
(6, 1006, 'Claudia', 'Mejía', '6543210987', '1988-02-28', 'Carrera 75, Cartagena, Colombia', '3112345678', 'claudia.mejia@horizontesdelsaber.edu.co', 'Especialización', 'Psicología', 9, '2024-10-15', 'por horas', 'Ciencias Sociales'),
(7, 1007, 'Andrés', 'Zuluaga', '7896541230', '1978-11-15', 'Avenida Siempre Viva, Bogotá, Colombia', '3187654321', 'andres.zuluaga@horizontesdelsaber.edu.co', 'Maestría', 'Economía', 18, '2024-01-30', 'tiempo completo', 'Ciencias Económicas'),
(8, 1008, 'María', 'Pérez', '5432109876', '1985-09-09', 'Calle Principal, Pereira, Colombia', '3103456789', 'maria.perez@horizontesdelsaber.edu.co', 'Doctorado', 'Química', 12, '2023-05-25', 'medio tiempo', 'Química Analítica'),
(9, 1009, 'Fernando', 'Cardona', '0123456789', '1992-01-25', 'Calle 18, Tunja, Colombia', '3165432109', 'fernando.cardona@horizontesdelsaber.edu.co', 'Licenciatura', 'Filosofía', 5, '2001-01-10', 'por horas', 'Filosofía y Letras'),
(10, 1010, 'Laura', 'Castro', '6789012345', '1980-10-30', 'Carrera 88, Medellín, Colombia', '3176543210', 'laura.castro@horizontesdelsaber.edu.co', 'Maestría', 'Literatura', 14, '2002-06-11', 'tiempo completo', 'Lenguas y Literatura');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `actividades_extracurriculares`
--
ALTER TABLE `actividades_extracurriculares`
  ADD PRIMARY KEY (`id_actividades_extracurriculares`),
  ADD KEY `id_profesores` (`id_profesores`);

--
-- Indices de la tabla `asignaturas`
--
ALTER TABLE `asignaturas`
  ADD PRIMARY KEY (`id_asignaturas`),
  ADD KEY `id_cursos` (`id_cursos`),
  ADD KEY `id_plan_estudio` (`id_plan_estudio`);

--
-- Indices de la tabla `aulas`
--
ALTER TABLE `aulas`
  ADD PRIMARY KEY (`id_aulas`),
  ADD UNIQUE KEY `numero_identificador` (`numero_identificador`);

--
-- Indices de la tabla `biblioteca`
--
ALTER TABLE `biblioteca`
  ADD PRIMARY KEY (`id_biblioteca`),
  ADD KEY `dni_estudiantes` (`dni_estudiantes`);

--
-- Indices de la tabla `calificaciones`
--
ALTER TABLE `calificaciones`
  ADD PRIMARY KEY (`id_calificaciones`),
  ADD KEY `dni_estudiante` (`dni_estudiante`),
  ADD KEY `id_cursos` (`id_cursos`),
  ADD KEY `id_asignaturas` (`id_asignaturas`);

--
-- Indices de la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD PRIMARY KEY (`id_cursos`),
  ADD KEY `id_profesores` (`id_profesores`),
  ADD KEY `id_aulas` (`id_aulas`);

--
-- Indices de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD PRIMARY KEY (`Id_estudiantes`),
  ADD UNIQUE KEY `dni` (`dni`);

--
-- Indices de la tabla `estudiantes_actividades_extracurriculares`
--
ALTER TABLE `estudiantes_actividades_extracurriculares`
  ADD PRIMARY KEY (`id_estudiantes_actividades_extracurriculares`),
  ADD KEY `dni_estudiante` (`dni_estudiante`),
  ADD KEY `id_actividades_extracurriculares` (`id_actividades_extracurriculares`);

--
-- Indices de la tabla `estudiantes_asignaturas`
--
ALTER TABLE `estudiantes_asignaturas`
  ADD PRIMARY KEY (`id_estudiantes_asignaturas`),
  ADD KEY `dni_estudiante` (`dni_estudiante`),
  ADD KEY `id_asignaturas` (`id_asignaturas`);

--
-- Indices de la tabla `estudiantes_cursos`
--
ALTER TABLE `estudiantes_cursos`
  ADD PRIMARY KEY (`id_estudiantes_cursos`),
  ADD KEY `dni_estudiante` (`dni_estudiante`),
  ADD KEY `id_cursos` (`id_cursos`);

--
-- Indices de la tabla `plan_estudio`
--
ALTER TABLE `plan_estudio`
  ADD PRIMARY KEY (`id_plan_estudio`),
  ADD KEY `id_cursos` (`id_cursos`);

--
-- Indices de la tabla `prestamos`
--
ALTER TABLE `prestamos`
  ADD PRIMARY KEY (`id_prestamos`),
  ADD KEY `id_biblioteca` (`id_biblioteca`),
  ADD KEY `dni_estudiantes` (`dni_estudiantes`),
  ADD KEY `id_profesores` (`id_profesores`);

--
-- Indices de la tabla `profesores`
--
ALTER TABLE `profesores`
  ADD PRIMARY KEY (`id_profesores`),
  ADD UNIQUE KEY `cod_empleado` (`cod_empleado`),
  ADD UNIQUE KEY `dni` (`dni`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `actividades_extracurriculares`
--
ALTER TABLE `actividades_extracurriculares`
  MODIFY `id_actividades_extracurriculares` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `asignaturas`
--
ALTER TABLE `asignaturas`
  MODIFY `id_asignaturas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `aulas`
--
ALTER TABLE `aulas`
  MODIFY `id_aulas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `biblioteca`
--
ALTER TABLE `biblioteca`
  MODIFY `id_biblioteca` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `calificaciones`
--
ALTER TABLE `calificaciones`
  MODIFY `id_calificaciones` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `cursos`
--
ALTER TABLE `cursos`
  MODIFY `id_cursos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  MODIFY `Id_estudiantes` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `estudiantes_actividades_extracurriculares`
--
ALTER TABLE `estudiantes_actividades_extracurriculares`
  MODIFY `id_estudiantes_actividades_extracurriculares` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `estudiantes_asignaturas`
--
ALTER TABLE `estudiantes_asignaturas`
  MODIFY `id_estudiantes_asignaturas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `estudiantes_cursos`
--
ALTER TABLE `estudiantes_cursos`
  MODIFY `id_estudiantes_cursos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `plan_estudio`
--
ALTER TABLE `plan_estudio`
  MODIFY `id_plan_estudio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `prestamos`
--
ALTER TABLE `prestamos`
  MODIFY `id_prestamos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `profesores`
--
ALTER TABLE `profesores`
  MODIFY `id_profesores` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `actividades_extracurriculares`
--
ALTER TABLE `actividades_extracurriculares`
  ADD CONSTRAINT `actividades_extracurriculares_ibfk_1` FOREIGN KEY (`id_profesores`) REFERENCES `profesores` (`id_profesores`) ON DELETE CASCADE;

--
-- Filtros para la tabla `asignaturas`
--
ALTER TABLE `asignaturas`
  ADD CONSTRAINT `asignaturas_ibfk_1` FOREIGN KEY (`id_cursos`) REFERENCES `cursos` (`id_cursos`) ON DELETE CASCADE,
  ADD CONSTRAINT `asignaturas_ibfk_2` FOREIGN KEY (`id_plan_estudio`) REFERENCES `plan_estudio` (`id_plan_estudio`) ON DELETE CASCADE;

--
-- Filtros para la tabla `biblioteca`
--
ALTER TABLE `biblioteca`
  ADD CONSTRAINT `biblioteca_ibfk_1` FOREIGN KEY (`dni_estudiantes`) REFERENCES `estudiantes` (`dni`) ON DELETE CASCADE;

--
-- Filtros para la tabla `calificaciones`
--
ALTER TABLE `calificaciones`
  ADD CONSTRAINT `calificaciones_ibfk_1` FOREIGN KEY (`dni_estudiante`) REFERENCES `estudiantes` (`dni`),
  ADD CONSTRAINT `calificaciones_ibfk_2` FOREIGN KEY (`id_cursos`) REFERENCES `cursos` (`id_cursos`),
  ADD CONSTRAINT `calificaciones_ibfk_3` FOREIGN KEY (`id_asignaturas`) REFERENCES `asignaturas` (`id_asignaturas`);

--
-- Filtros para la tabla `cursos`
--
ALTER TABLE `cursos`
  ADD CONSTRAINT `cursos_ibfk_1` FOREIGN KEY (`id_profesores`) REFERENCES `profesores` (`id_profesores`) ON DELETE CASCADE,
  ADD CONSTRAINT `cursos_ibfk_2` FOREIGN KEY (`id_aulas`) REFERENCES `aulas` (`id_aulas`) ON DELETE CASCADE;

--
-- Filtros para la tabla `estudiantes_actividades_extracurriculares`
--
ALTER TABLE `estudiantes_actividades_extracurriculares`
  ADD CONSTRAINT `estudiantes_actividades_extracurriculares_ibfk_1` FOREIGN KEY (`dni_estudiante`) REFERENCES `estudiantes` (`dni`) ON DELETE CASCADE,
  ADD CONSTRAINT `estudiantes_actividades_extracurriculares_ibfk_2` FOREIGN KEY (`id_actividades_extracurriculares`) REFERENCES `actividades_extracurriculares` (`id_actividades_extracurriculares`) ON DELETE CASCADE;

--
-- Filtros para la tabla `estudiantes_asignaturas`
--
ALTER TABLE `estudiantes_asignaturas`
  ADD CONSTRAINT `estudiantes_asignaturas_ibfk_1` FOREIGN KEY (`dni_estudiante`) REFERENCES `estudiantes` (`dni`) ON DELETE CASCADE,
  ADD CONSTRAINT `estudiantes_asignaturas_ibfk_2` FOREIGN KEY (`id_asignaturas`) REFERENCES `asignaturas` (`id_asignaturas`) ON DELETE CASCADE;

--
-- Filtros para la tabla `estudiantes_cursos`
--
ALTER TABLE `estudiantes_cursos`
  ADD CONSTRAINT `estudiantes_cursos_ibfk_1` FOREIGN KEY (`dni_estudiante`) REFERENCES `estudiantes` (`dni`) ON DELETE CASCADE,
  ADD CONSTRAINT `estudiantes_cursos_ibfk_2` FOREIGN KEY (`id_cursos`) REFERENCES `cursos` (`id_cursos`) ON DELETE CASCADE;

--
-- Filtros para la tabla `plan_estudio`
--
ALTER TABLE `plan_estudio`
  ADD CONSTRAINT `plan_estudio_ibfk_1` FOREIGN KEY (`id_cursos`) REFERENCES `cursos` (`id_cursos`) ON DELETE CASCADE;

--
-- Filtros para la tabla `prestamos`
--
ALTER TABLE `prestamos`
  ADD CONSTRAINT `prestamos_ibfk_1` FOREIGN KEY (`id_biblioteca`) REFERENCES `biblioteca` (`id_biblioteca`) ON DELETE CASCADE,
  ADD CONSTRAINT `prestamos_ibfk_2` FOREIGN KEY (`dni_estudiantes`) REFERENCES `estudiantes` (`dni`) ON DELETE CASCADE,
  ADD CONSTRAINT `prestamos_ibfk_3` FOREIGN KEY (`id_profesores`) REFERENCES `profesores` (`id_profesores`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
