/*
 * generated by Xtext 2.10.0
 */
package com.fastpilot.jaus.cjsidl


/**
 * Initialization support for running Xtext languages without Equinox extension registry.
 */
class JausStandaloneSetup extends JausStandaloneSetupGenerated {

	def static void doSetup() {
		new JausStandaloneSetup().createInjectorAndDoEMFRegistration()
	}
}
