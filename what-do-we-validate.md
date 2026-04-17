1. **Is the infrastructure defective?**  
    We are delivering an AI Factory in the customer’s environment, and that means validating that the hardware is not defective when it is assembled together as a single system. This includes identifying hardware that fails to meet performance expectations in larger-scale or multi-node GPU-to-GPU scenarios. When hardware does not meet those standards, part of our role is to identify it and drive replacement or remediation.

2. **Is the infrastructure defective?**  
    Infrastructure includes the hardware, but it also includes foundational software components required to support the environment. This includes items such as the operating system, Kubernetes, Calico, network operators, drivers, and similar platform-level components. These elements must be installed, configured, and validated correctly in order for higher-level applications to function properly.
    
3. **Is the solution defective?**  
    If we sold the customer a solution, and that solution does not function as intended when assembled according to the prescribed design, then that is a problem we need to identify and address. Even when we are working from an approved reference architecture or validated design, we should not assume that successful installation alone is sufficient. Basic end-to-end validation is necessary to confirm that the major components work together in the customer environment.
    
4. **Is the work product defective?**  
    If our team installs or configures a component, we should perform an appropriate baseline test to verify that the work was completed correctly. It is not reasonable to treat installation as in scope while treating all meaningful validation as out of scope. At a minimum, our deliverables should include enough testing to demonstrate that our implementation is sound and does not leave the customer with rework or rollback as the next step.
    
5. **Is the application itself defective?**  
    Applications such as Run:AI run on top of the underlying infrastructure. Like any software product, they may contain bugs or limitations. In general, our team is not responsible for exhaustive application-level bug testing, deep product QA, or validating every possible customization unless that work is explicitly included in the statement of work.