class TermsController < SiteController

  def new
    required_terms
    new_terms
  end

  def new_terms
    @user = session_user
    if @user
      if @user.terms.empty?
        #TODO would like this to show the terms they have already accepted
        redirect_to legal_site_terms_path and return
      end

      @term = Term.new
    else
      redirect_to login_path
    end
  end

  def create
    @user = session_user
    @term = Term.new
    if @user
      # removed for now (undefined pretty_inspect)
      # logger.debug "Accepting terms for user #{@user.pretty_inspect}"

      @user.accept_terms unless @user.terms.empty?

      if @user.errors.empty?
        redirect_to terms_redirect
      else
        logger.debug "Found errors, updating terms object with #{@user.errors}"
        @user.errors.each do |attr, message|
          @term.errors.add(attr, message)
        end
        render :new
      end
    else
      redirect_to login_path
    end
  end

  protected
    def required_terms
      @term_description ||= {
        'OpenShift Online Services Agreement' => 'This agreement contains the terms and conditions that apply to your access and use of the OpenShift Online Services and Software. The Agreement also incorporates the Acceptable Use Policy which can be reviewed at http://www.openshift.com/legal.',
        'Red Hat Portals Terms of Use' => 'These terms apply to the extent you use the Red Hat Customer Portal website.'
      }
    end
end
