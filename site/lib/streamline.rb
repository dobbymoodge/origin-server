#
# This mixin encapsulates calls made back to the IT systems via
# the streamline REST service.
#
module Streamline

  class Error < StandardError
    attr :exit_code
    def initialize(exit_code=nil, message=nil)
      super(message)
      @exit_code = exit_code
    end
  end

  class UserException < Error; end

  class UserValidationException < Error; end

  class StreamlineException < Error
    def initialize(message=nil)
      super(144, message)
    end
  end

  # Raised when the reset token has already been used
  class TokenExpired < StreamlineException; end

  # The user name or password is invalid
  class AuthenticationDenied < StreamlineException; end

  # The secretKey used for an API transaction was incorrect
  class PromoteInvalidSecretKey < StreamlineException; end

  # The attr_streamline method was called incorrectly
  class FullUserClassError < StreamlineException; end
end
