RedHatCloud::Application.routes.draw do

  community_paas = redirect('/community/paas')
  get_started = redirect('/community/get-started')
  open_source_download = redirect('/community/open-source/download-origin')

  # Legacy content redirects
  match 'access/express(/:request)' => community_paas
  match 'access/flex(/:request)' => community_paas
  match 'features' => community_paas, :as => 'features'
  match 'power' => community_paas
  match 'about' => community_paas, :as => 'about'
  match 'express' => community_paas, :as => 'express'
  match 'flex' => community_paas, :as => 'flex'
  match 'flex_redirect' => community_paas, :as => 'flex_redirect'
  match 'platform' => community_paas
  match 'partners' => redirect('/community/partners')

  match 'getting_started' => get_started
  match 'getting_started/express' => get_started
  match 'getting_started/flex' => get_started

  match 'getting_started_external/:registration_referrer' => 'getting_started_external#show'

  # Legacy account creation paths
  match 'email_confirm_flex' => app_redirect {|p, req| "email_confirm?#{req.query_string}"}
  match 'email_confirm_express' => app_redirect {|p, req| "email_confirm?#{req.query_string}"}
  match 'user/new' => app_redirect('account/new'), :via => [:get]
  match 'user/new/flex' => app_redirect('account/new'), :via => [:get]
  match 'user/new/express' => app_redirect('account/new'), :via => [:get]
  match 'user/complete' => app_redirect('account/complete'), :via => [:get]

  match 'account/plans' => app_redirect('account/plan'), :via => [:get]

  # Prototype not found pages
  match 'not_found' => 'product#not_found'
  match 'error' => 'product#error'
  match 'console/not_found' => 'product#console_not_found'
  match 'console/error' => 'product#console_error'

  # Buzz
  match 'twitter/latest_tweets' => 'twitter#latest_tweets'
  match 'twitter/latest_retweets' => 'twitter#latest_retweets'

  resource :account,
           :controller => :account,
           :only => [:new, :create, :show] do

    get :complete, :on => :member

    if Rails.configuration.aria_enabled
      resources :plans,   :only => :index do
        resource :upgrade, :controller => :account_upgrades, :only => [:edit, :new, :create, :show] do
          put  :edit, :action => :update, :on => :member

          resource :payment_method,
                   :controller => :account_upgrade_payment_method,
                   :only => [:show, :new, :edit] do
            get :direct_create, :on => :member
            get :direct_update, :on => :member
          end
          resource :billing_info,
                   :controller => :account_upgrade_billing_info,
                   :only => :edit do
            put :edit, :action => :update, :on => :member
          end
        end
      end
      resource :payment_method, :only => [:edit] do
        get :direct_update, :on => :member
      end
      resource :billing_info,
               :controller => :billing_info,
               :only => :edit do
        put :edit, :action => :update, :on => :member
      end
      resource :plan, :only => [:update, :show]
    end

    resource  :password, :controller => :password do
      match 'edit' => 'password#update', :via => :put
      member do
        get :reset
        get :success
      end
    end
  end

  scope 'account' do
    resource :domain, :only => [:new, :create, :edit, :update]
    resources :keys, :only => [:new, :create, :destroy]
  end

  match 'account/help' => 'account#help', :via => [:get]

  match 'user/create/external' => 'account#create_external', :via => [:post]

  match 'user/reset_password' => app_redirect {|p, req| "account/password/reset?#{req.query_string}"}, :via => [:get]
  match 'email_confirm' => 'email_confirm#confirm'
  match 'email_confirm_external/:registration_referrer' => 'email_confirm#confirm_external'

  match 'user' => app_redirect('account/new'), :via => [:get]

  resource :terms,
           :as => "terms",
           :controller => "terms",
           :path_names => { :new => 'accept' },
           :only => [:new, :create]

  match 'legal/acceptance_terms' => 'terms#acceptance_terms', :as => 'acceptance_terms'

  match 'legal' => redirect('/community/legal')
  match 'legal/site_terms' => redirect('/community/legal/site_terms')
  match 'legal/services_agreement' => redirect('/community/legal/services_agreement')
  match 'legal/acceptable_use' => redirect('/community/legal/acceptable_use')
  match 'legal/openshift_privacy' => redirect('/community/legal/openshift_privacy')

  resource :login,
           :controller => "login",
           :only => [:show, :create]
  match 'login/flex' => 'login#show_flex', :via => [:get]
  match 'login/express' => 'login#show_express', :via => [:get]

  resource :logout,
           :controller => "logout",
           :only => [:show]
  match 'logout/flex' => 'logout#show_flex', :via => [:get]
  match 'logout/express' => 'logout#show_express', :via => [:get]

  scope 'console' do
    openshift_console :skip => :account
  end

  match 'new_application' => 'application_types#index', :via => :get

  match 'opensource' => open_source_download
  match 'opensource/download' => open_source_download
  resources   :download,
              :controller => 'download',
              :only => [:show,:index]

  unless Rails.env.production?
    match 'styleguide/:action' => 'styleguide'
    match 'styleguide' => 'styleguide#index'
  end

  root :to => "product#index"

  scope 'status' do
    match '/(:base)(.:format)' => StatusApp, :as => 'status'
    match '/status.js' => StatusApp, :as => 'status_js'
    match '/open_issues.js' => StatusApp, :as => 'open_issues_js'
    match '/sync/(:host)' => StatusApp, :constraints => {:host => /[0-z\.-]+/}
  end
end
