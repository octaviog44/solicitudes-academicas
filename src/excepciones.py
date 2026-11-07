
class SolicitudError(Exception):
    """Base para errores del dominio de solicitudes."""


class SolicitudInvalidaError(SolicitudError):
    """Los datos de entrada no son válidos."""


class SolicitudNoEncontradaError(SolicitudError):
    """No existe una solicitud con el id indicado."""