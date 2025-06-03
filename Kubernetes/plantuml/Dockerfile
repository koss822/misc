FROM ubuntu:24.04

# Environment configuration
ENV CATALINA_HOME=/opt/tomcat
ENV PATH=$CATALINA_HOME/bin:$PATH
ENV JAVA_OPTS="-Xms512m -Xmx1024m -XX:MaxMetaspaceSize=256m"

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    openjdk-21-jdk \
    ca-certificates \
    wget \
    unzip && \
    rm -rf /var/lib/apt/lists/*

# Create tomcat user
RUN groupadd -r tomcat && \
    useradd -r -g tomcat -d /opt/tomcat -s /bin/false tomcat

# Install Tomcat
ARG TOMCAT_VERSION=10.0.20
RUN wget -O /tmp/tomcat.tar.gz \
    https://archive.apache.org/dist/tomcat/tomcat-10/v${TOMCAT_VERSION}/bin/apache-tomcat-${TOMCAT_VERSION}.tar.gz && \
    mkdir -p /opt/tomcat && \
    tar xzf /tmp/tomcat.tar.gz -C /opt/tomcat --strip-components=1 && \
    sed -i '/<Engine name="Catalina" defaultHost="localhost">/a \
        <Valve className="org.apache.catalina.valves.HealthCheckValve" \
               path="/health" \
               showDetails="false" \
               checkContainersAvailable="true"/>' /opt/tomcat/conf/server.xml && \
    chown -R tomcat:tomcat /opt/tomcat && \
    chmod -R u+rX /opt/tomcat

# Deploy WAR file
ARG WAR_URL="https://github.com/plantuml/plantuml-server/releases/download/v1.2025.0/plantuml-jsp-v1.2025.0.war"
RUN wget -O /opt/tomcat/webapps/ROOT.war "${WAR_URL}" && \
    rm -rf /opt/tomcat/webapps/ROOT

# Final configuration
RUN chmod -R 750 $CATALINA_HOME/conf && \
    chmod -R 750 $CATALINA_HOME/logs

USER tomcat
EXPOSE 8080
CMD ["catalina.sh", "run"]
